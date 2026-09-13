/**
 * dashboard.js
 * ------------
 * Chart.js visualizations for the Data Analysis Dashboard page.
 *
 * Charts rendered:
 *   1. Feature Means       — horizontal bar chart
 *   2. Revenue Distribution — bar chart (histogram bins)
 *   3. Correlations        — horizontal bar chart
 *   4. Correlation bars    — custom HTML bars (no chart needed)
 *   5. Scatter: Previous Revenue vs Revenue
 *   6. Scatter: Number of Customers vs Revenue
 *   7. Scatter: Marketing Spend vs Revenue
 *   8. Scatter: Discount Percentage vs Revenue
 *
 * All data is hardcoded from the EDA results (Phase 3).
 * In Phase 9 these values could optionally be fetched from the backend.
 */

'use strict';

// ── Chart.js global defaults ──────────────────────────────────────────────────
Chart.defaults.font.family = "-apple-system, 'Segoe UI', system-ui, sans-serif";
Chart.defaults.font.size   = 12;
Chart.defaults.color       = '#57606a';

// ── EDA data (from Phase 3 analysis) ─────────────────────────────────────────
const FEATURE_MEANS = {
  'Marketing Spend':      25527,
  'Advertising Spend':    15354,
  'Website Traffic':      89768,
  'No. of Customers':     2000,
  'Product Price':        256,
  'Discount %':           25.2,
  'Previous Revenue':     256889,
};

const CORRELATIONS = [
  { label: 'previous_revenue',      value: 0.824 },
  { label: 'number_of_customers',   value: 0.373 },
  { label: 'marketing_spend',       value: 0.291 },
  { label: 'advertising_spend',     value: 0.217 },
  { label: 'website_traffic',       value: 0.144 },
  { label: 'product_price',         value: 0.038 },
  { label: 'discount_percentage',   value: -0.049 },
];

// Revenue distribution bins (approximate histogram data from EDA)
// x = bin midpoint (USD), y = approximate count
const REVENUE_BINS = [
  { x: 40000,  y: 15  },
  { x: 60000,  y: 50  },
  { x: 80000,  y: 120 },
  { x: 100000, y: 250 },
  { x: 120000, y: 430 },
  { x: 140000, y: 640 },
  { x: 160000, y: 780 },
  { x: 180000, y: 700 },
  { x: 200000, y: 550 },
  { x: 220000, y: 430 },
  { x: 240000, y: 330 },
  { x: 260000, y: 220 },
  { x: 280000, y: 150 },
  { x: 300000, y: 80  },
  { x: 320000, y: 35  },
  { x: 340000, y: 10  },
];

// Scatter sample data (100 representative points per chart)
// Generated to match the real distribution patterns
function generateScatterSample(correlation, n, xRange, xMean, xStd, yMean, yStd) {
  const points = [];
  const rng = mulberry32(42);
  for (let i = 0; i < n; i++) {
    const z1 = boxMuller(rng);
    const z2 = boxMuller(rng);
    const x = xMean + xStd * z1;
    const y = yMean + yStd * (correlation * z1 + Math.sqrt(1 - correlation ** 2) * z2);
    if (x >= xRange[0] && x <= xRange[1]) {
      points.push({ x: Math.round(x), y: Math.round(Math.max(y, 5000)) });
    }
  }
  return points;
}

// Simple seeded random number generator (Mulberry32)
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function boxMuller(rng) {
  const u1 = rng(), u2 = rng();
  return Math.sqrt(-2 * Math.log(u1 + 1e-10)) * Math.cos(2 * Math.PI * u2);
}

const scatterPrevRevenue  = generateScatterSample(0.824, 300, [20000, 500000], 256889, 138396, 165609, 51202);
const scatterCustomers    = generateScatterSample(0.373, 300, [100,   5000],   2000,   869,    165609, 51202);
const scatterMarketing    = generateScatterSample(0.291, 300, [1000,  50000],  25527,  14142,  165609, 51202);
const scatterDiscount     = generateScatterSample(-0.049, 300, [0, 50],        25.2,   14.3,   165609, 51202);


// ── 1. Feature Means Chart ────────────────────────────────────────────────────
(function renderFeatureMeans() {
  const ctx = document.getElementById('chart-feature-means');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(FEATURE_MEANS),
      datasets: [{
        label: 'Mean Value',
        data: Object.values(FEATURE_MEANS),
        backgroundColor: 'rgba(59, 130, 212, 0.75)',
        borderColor: 'rgba(59, 130, 212, 1)',
        borderWidth: 1,
        borderRadius: 4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => {
              const v = ctx.raw;
              if (ctx.label === 'Discount %') return ` ${v.toFixed(1)}%`;
              if (['No. of Customers'].includes(ctx.label)) return ` ${v.toLocaleString()}`;
              return ` $${v.toLocaleString()}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: {
            callback: v => v >= 1000 ? `$${(v/1000).toFixed(0)}K` : v,
          }
        },
        y: { grid: { display: false } }
      }
    }
  });
})();


// ── 2. Revenue Distribution Chart ────────────────────────────────────────────
(function renderRevenueDist() {
  const ctx = document.getElementById('chart-revenue-dist');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: REVENUE_BINS.map(b => `$${(b.x/1000).toFixed(0)}K`),
      datasets: [{
        label: 'Count',
        data: REVENUE_BINS.map(b => b.y),
        backgroundColor: 'rgba(59, 130, 212, 0.7)',
        borderColor: 'rgba(59, 130, 212, 1)',
        borderWidth: 1,
        borderRadius: 3,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { title: t => `Revenue bin: ${t[0].label}` } },
        annotation: undefined,
      },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: 'rgba(0,0,0,0.05)' }, title: { display: true, text: 'Count' } }
      }
    }
  });
})();


// ── 3. Correlations Chart ─────────────────────────────────────────────────────
(function renderCorrelations() {
  const ctx = document.getElementById('chart-correlations');
  if (!ctx) return;

  const sorted = [...CORRELATIONS].sort((a, b) => a.value - b.value);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sorted.map(c => c.label),
      datasets: [{
        label: 'Correlation with Revenue',
        data: sorted.map(c => c.value),
        backgroundColor: sorted.map(c =>
          c.value >= 0
            ? 'rgba(59, 130, 212, 0.75)'
            : 'rgba(220, 38, 38, 0.75)'
        ),
        borderColor: sorted.map(c =>
          c.value >= 0 ? 'rgba(59,130,212,1)' : 'rgba(220,38,38,1)'
        ),
        borderWidth: 1,
        borderRadius: 4,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` r = ${ctx.raw.toFixed(3)}` } }
      },
      scales: {
        x: {
          min: -0.2,
          max: 1.0,
          grid: { color: 'rgba(0,0,0,0.05)' },
          title: { display: true, text: 'Pearson Correlation Coefficient' }
        },
        y: { grid: { display: false } }
      }
    }
  });
})();


// ── 4. Correlation HTML Bars ──────────────────────────────────────────────────
(function renderCorrBars() {
  const container = document.getElementById('corr-bars');
  if (!container) return;

  CORRELATIONS.forEach(({ label, value }) => {
    const isNeg = value < 0;
    const width = Math.round(Math.abs(value) * 100);
    const row = document.createElement('div');
    row.className = 'corr-row';
    row.innerHTML = `
      <span class="corr-name">${label}</span>
      <div class="corr-track">
        <div class="corr-fill${isNeg ? ' negative' : ''}" style="width:${width}%"></div>
      </div>
      <span class="corr-val">${value >= 0 ? '+' : ''}${value.toFixed(3)}</span>
    `;
    container.appendChild(row);
  });
})();


// ── 5–8. Scatter Charts ───────────────────────────────────────────────────────
function renderScatter(canvasId, points, xLabel, yLabel, color) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: `${xLabel} vs Revenue`,
        data: points,
        backgroundColor: color || 'rgba(59, 130, 212, 0.35)',
        pointRadius: 3,
        pointHoverRadius: 4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => `(${ctx.parsed.x.toLocaleString()}, $${ctx.parsed.y.toLocaleString()})`
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: xLabel },
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: { maxTicksLimit: 6, callback: v => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v }
        },
        y: {
          title: { display: true, text: 'Revenue (USD)' },
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: { callback: v => `$${(v/1000).toFixed(0)}K` }
        }
      }
    }
  });
}

renderScatter('chart-scatter-prev',      scatterPrevRevenue, 'Previous Revenue (USD)', 'Revenue');
renderScatter('chart-scatter-customers', scatterCustomers,   'Number of Customers',    'Revenue');
renderScatter('chart-scatter-marketing', scatterMarketing,   'Marketing Spend (USD)',  'Revenue');
renderScatter('chart-scatter-discount',  scatterDiscount,    'Discount Percentage (%)', 'Revenue', 'rgba(220,38,38,0.35)');
