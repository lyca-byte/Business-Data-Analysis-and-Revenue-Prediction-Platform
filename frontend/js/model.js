/**
 * model.js
 * --------
 * Chart.js visualizations for the Model Performance page.
 *
 * Charts rendered:
 *   1. Validation vs Test metrics comparison (grouped bar)
 *   2. R² interpretation reference chart (horizontal bar)
 *   3. Feature coefficients (horizontal bar)
 *
 * On page load, attempts to fetch live metrics from GET /model-info.
 * If the backend is unreachable, falls back to hardcoded Phase 6 values.
 */

'use strict';

Chart.defaults.font.family = "-apple-system, 'Segoe UI', system-ui, sans-serif";
Chart.defaults.font.size   = 12;
Chart.defaults.color       = '#57606a';

// ── Model metrics from Phase 6 ────────────────────────────────────────────────
const VAL_METRICS = { mae: 14127.9,  mse: 299508040.77, rmse: 17306.3,  r2: 0.8877 };
const TEST_METRICS = { mae: 14127.04, mse: 295075947.15, rmse: 17177.77, r2: 0.8847 };

const COEFFICIENTS = {
  'previous_revenue':      41567.98,
  'number_of_customers':   17576.15,
  'marketing_spend':       10999.16,
  'advertising_spend':      4590.92,
  'product_price':          2148.70,
  'website_traffic':        1867.78,
  'discount_percentage':   -2942.84,
};


// ── 1. Validation vs Test Comparison Chart ────────────────────────────────────
(function renderMetricsComparison() {
  const ctx = document.getElementById('chart-metrics-comparison');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['MAE ($)', 'RMSE ($)', 'R² Score'],
      datasets: [
        {
          label: 'Validation',
          data: [VAL_METRICS.mae, VAL_METRICS.rmse, VAL_METRICS.r2 * 20000],
          backgroundColor: 'rgba(217, 119, 6, 0.7)',
          borderColor: 'rgba(217, 119, 6, 1)',
          borderWidth: 1,
          borderRadius: 4,
        },
        {
          label: 'Test',
          data: [TEST_METRICS.mae, TEST_METRICS.rmse, TEST_METRICS.r2 * 20000],
          backgroundColor: 'rgba(59, 130, 212, 0.7)',
          borderColor: 'rgba(59, 130, 212, 1)',
          borderWidth: 1,
          borderRadius: 4,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        tooltip: {
          callbacks: {
            label: ctx => {
              // R² was scaled by 20000 for display; unscale for tooltip
              if (ctx.label === 'R² Score') return ` R² = ${(ctx.raw / 20000).toFixed(4)}`;
              return ` $${ctx.raw.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
            }
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: {
            callback: v => v >= 1000 ? `$${(v/1000).toFixed(0)}K` : v
          }
        }
      }
    }
  });
})();


// ── 2. R² Interpretation Chart ────────────────────────────────────────────────
(function renderR2Interpretation() {
  const ctx = document.getElementById('chart-r2-interpretation');
  if (!ctx) return;

  const levels = [
    { label: 'Perfect (1.0)',    value: 1.00 },
    { label: 'Excellent (0.95)', value: 0.95 },
    { label: 'Our Model (0.885)',value: 0.885 },
    { label: 'Good (0.80)',      value: 0.80 },
    { label: 'Moderate (0.60)', value: 0.60 },
    { label: 'Weak (0.30)',      value: 0.30 },
    { label: 'No better (0.0)', value: 0.00 },
  ];

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: levels.map(l => l.label),
      datasets: [{
        label: 'R² Score',
        data: levels.map(l => l.value),
        backgroundColor: levels.map(l =>
          l.label.includes('Our Model')
            ? 'rgba(22, 163, 74, 0.85)'
            : 'rgba(59, 130, 212, 0.45)'
        ),
        borderColor: levels.map(l =>
          l.label.includes('Our Model')
            ? 'rgba(22, 163, 74, 1)'
            : 'rgba(59, 130, 212, 0.7)'
        ),
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ` R² = ${ctx.raw.toFixed(3)}` } }
      },
      scales: {
        x: {
          min: 0, max: 1.05,
          title: { display: true, text: 'R² Score' },
          grid: { color: 'rgba(0,0,0,0.05)' }
        },
        y: { grid: { display: false } }
      }
    }
  });
})();


// ── 3. Feature Coefficients Chart ─────────────────────────────────────────────
(function renderCoefficients() {
  const ctx = document.getElementById('chart-coefficients');
  if (!ctx) return;

  // Sort by coefficient value ascending for a clear horizontal bar
  const entries = Object.entries(COEFFICIENTS).sort((a, b) => a[1] - b[1]);
  const labels = entries.map(([k]) => k);
  const values = entries.map(([, v]) => v);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Coefficient (scaled features)',
        data: values,
        backgroundColor: values.map(v =>
          v >= 0 ? 'rgba(59, 130, 212, 0.75)' : 'rgba(220, 38, 38, 0.75)'
        ),
        borderColor: values.map(v =>
          v >= 0 ? 'rgba(59,130,212,1)' : 'rgba(220,38,38,1)'
        ),
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ` Coefficient: ${ctx.raw >= 0 ? '+' : ''}${ctx.raw.toLocaleString(undefined, { maximumFractionDigits: 0 })}`
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(0,0,0,0.05)' },
          title: { display: true, text: 'Coefficient Value (StandardScaled features)' },
          ticks: { callback: v => v >= 1000 || v <= -1000 ? `${(v/1000).toFixed(0)}K` : v }
        },
        y: { grid: { display: false } }
      }
    }
  });
})();


// ── Live data from backend (Phase 9) ─────────────────────────────────────────
// Fetches /model-info and updates the metric cards with live values.
// Falls back to hardcoded values silently if the backend is not running.

/**
 * Update a metric card's displayed value.
 * @param {string} cardSelector - CSS selector for the card element
 * @param {string} valueSelector - CSS selector for the value element within the card
 * @param {string} newValue - The new text to display
 */
function updateMetricCard(valueSelector, newValue) {
  const el = document.querySelector(valueSelector);
  if (el) el.textContent = newValue;
}

async function loadLiveModelInfo() {
  // api.js must be loaded before model.js — it is included via model.html
  if (typeof getModelInfo !== 'function') return;

  try {
    const info = await getModelInfo();
    const vm   = info.validation_metrics;
    const tm   = info.test_metrics;

    // ── Update the backend connection status banner ────────────────────────
    const banner = document.getElementById('api-connection-banner');
    if (banner) {
      banner.textContent = 'Live data loaded from backend API.';
      banner.className   = 'alert alert-success text-sm mb-2';
      banner.classList.remove('hidden');
    }

    // ── Update model info table values ────────────────────────────────────
    const trainingDateEl = document.getElementById('live-training-date');
    if (trainingDateEl) trainingDateEl.textContent = info.training_date || '—';

    const sklearnEl = document.getElementById('live-sklearn-version');
    if (sklearnEl && info.library_versions) {
      sklearnEl.textContent = `scikit-learn ${info.library_versions.scikit_learn}`;
    }

    // ── Update validation metric cards ─────────────────────────────────────
    // Metric card values are identified by data-metric attributes
    document.querySelectorAll('[data-val-metric]').forEach(el => {
      const key = el.getAttribute('data-val-metric');
      if (vm[key] !== undefined) {
        if (key === 'r2') {
          el.textContent = vm[key].toFixed(4);
        } else if (key === 'mse') {
          el.textContent = '$' + (vm[key] / 1e6).toFixed(1) + 'M';
        } else {
          el.textContent = '$' + vm[key].toLocaleString('en-US', { maximumFractionDigits: 0 });
        }
      }
    });

    // ── Update test metric cards ───────────────────────────────────────────
    document.querySelectorAll('[data-test-metric]').forEach(el => {
      const key = el.getAttribute('data-test-metric');
      if (tm[key] !== undefined) {
        if (key === 'r2') {
          el.textContent = tm[key].toFixed(4);
        } else if (key === 'mse') {
          el.textContent = '$' + (tm[key] / 1e6).toFixed(1) + 'M';
        } else {
          el.textContent = '$' + tm[key].toLocaleString('en-US', { maximumFractionDigits: 0 });
        }
      }
    });

  } catch (_) {
    // Backend not reachable — hardcoded values remain displayed
    const banner = document.getElementById('api-connection-banner');
    if (banner) {
      banner.textContent = 'Backend not reachable. Showing static metrics from training.';
      banner.className   = 'alert alert-error text-sm mb-2';
      banner.classList.remove('hidden');
    }
  }
}

// Run on page load
loadLiveModelInfo();
