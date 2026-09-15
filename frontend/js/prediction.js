/**
 * prediction.js
 * -------------
 * Handles the Prediction page:
 *   - Form validation
 *   - API call to POST /predict (via api.js)
 *   - Displaying the prediction result
 *   - Chart.js revenue comparison chart
 *   - Sample data loader
 *   - CSV and JSON download
 */

'use strict';

// ── Sample business inputs ────────────────────────────────────────────────────
const SAMPLES = {
  small: {
    marketing_spend:     3000,
    advertising_spend:   1500,
    website_traffic:     15000,
    number_of_customers: 250,
    product_price:       35,
    discount_percentage: 20,
    previous_revenue:    45000,
  },
  medium: {
    marketing_spend:     12000,
    advertising_spend:   6000,
    website_traffic:     60000,
    number_of_customers: 1500,
    product_price:       80,
    discount_percentage: 10,
    previous_revenue:    180000,
  },
  large: {
    marketing_spend:     35000,
    advertising_spend:   20000,
    website_traffic:     150000,
    number_of_customers: 4000,
    product_price:       220,
    discount_percentage: 5,
    previous_revenue:    420000,
  },
};

// ── State ─────────────────────────────────────────────────────────────────────
let lastPredictionResult = null;  // Stores the last API response for download
let revenueComparisonChart = null; // Chart.js instance (destroyed on re-render)

// ── DOM references ────────────────────────────────────────────────────────────
const form             = document.getElementById('prediction-form');
const btnPredict       = document.getElementById('btn-predict');
const btnReset         = document.getElementById('btn-reset');
const loadingState     = document.getElementById('loading-state');
const apiStatus        = document.getElementById('api-status');
const resultPlaceholder = document.getElementById('result-placeholder');
const resultPanel      = document.getElementById('result-panel');
const resultValue      = document.getElementById('result-value');
const resultModelInfo  = document.getElementById('result-model-info');
const inputSummaryBody = document.getElementById('input-summary-body');
const btnDownloadCsv   = document.getElementById('btn-download-csv');
const btnDownloadJson  = document.getElementById('btn-download-json');

// ── Validation rules ──────────────────────────────────────────────────────────
// These mirror the Pydantic validation rules in backend/schemas/prediction.py
const VALIDATION_RULES = {
  marketing_spend:     { min: 0,    max: null, required: true, label: 'Marketing Spend' },
  advertising_spend:   { min: 0,    max: null, required: true, label: 'Advertising Spend' },
  website_traffic:     { min: 0,    max: null, required: true, label: 'Website Traffic' },
  number_of_customers: { min: 0,    max: null, required: true, label: 'Number of Customers' },
  product_price:       { min: 0.01, max: null, required: true, label: 'Product Price' },
  discount_percentage: { min: 0,    max: 100,  required: true, label: 'Discount Percentage' },
  previous_revenue:    { min: 0,    max: null, required: true, label: 'Previous Revenue' },
};

// ── Form validation ───────────────────────────────────────────────────────────
function validateForm() {
  let isValid = true;

  Object.entries(VALIDATION_RULES).forEach(([fieldId, rules]) => {
    const input = document.getElementById(fieldId);
    const errorEl = document.getElementById(`err-${fieldId}`);
    const value = parseFloat(input.value);

    let errorMsg = '';

    if (input.value.trim() === '' || isNaN(value)) {
      errorMsg = `${rules.label} is required.`;
    } else if (value < rules.min) {
      errorMsg = `${rules.label} must be >= ${rules.min}.`;
    } else if (rules.max !== null && value > rules.max) {
      errorMsg = `${rules.label} must be <= ${rules.max}.`;
    }

    if (errorMsg) {
      input.classList.add('error');
      errorEl.textContent = errorMsg;
      errorEl.classList.add('visible');
      isValid = false;
    } else {
      input.classList.remove('error');
      errorEl.classList.remove('visible');
    }
  });

  return isValid;
}

// Clear a single field's error on input
Object.keys(VALIDATION_RULES).forEach(fieldId => {
  const input = document.getElementById(fieldId);
  if (!input) return;
  input.addEventListener('input', () => {
    input.classList.remove('error');
    const errorEl = document.getElementById(`err-${fieldId}`);
    if (errorEl) errorEl.classList.remove('visible');
    hideApiStatus();
  });
});

// ── Collect form values ───────────────────────────────────────────────────────
function getFormValues() {
  const data = {};
  Object.keys(VALIDATION_RULES).forEach(fieldId => {
    data[fieldId] = parseFloat(document.getElementById(fieldId).value);
  });
  return data;
}

// ── Load sample data ──────────────────────────────────────────────────────────
function loadSample(sampleKey) {
  const sample = SAMPLES[sampleKey];
  if (!sample) return;
  Object.entries(sample).forEach(([fieldId, value]) => {
    const input = document.getElementById(fieldId);
    if (input) {
      input.value = value;
      input.classList.remove('error');
      const errorEl = document.getElementById(`err-${fieldId}`);
      if (errorEl) errorEl.classList.remove('visible');
    }
  });
  hideApiStatus();
}

// ── UI helpers ────────────────────────────────────────────────────────────────
function showLoading() {
  btnPredict.disabled = true;
  loadingState.classList.add('visible');
}

function hideLoading() {
  btnPredict.disabled = false;
  loadingState.classList.remove('visible');
}

function showApiStatus(message, type = 'error') {
  apiStatus.textContent = message;
  apiStatus.className = `alert alert-${type} mt-2`;
  apiStatus.classList.remove('hidden');
}

function hideApiStatus() {
  apiStatus.classList.add('hidden');
}

// ── Display prediction result ─────────────────────────────────────────────────
function displayResult(predictionResponse, inputData) {
  const { predicted_revenue, model, model_type } = predictionResponse;

  // Show result panel, hide placeholder
  resultPlaceholder.classList.add('hidden');
  resultPanel.classList.remove('hidden');

  // Predicted revenue value
  resultValue.textContent = formatCurrency(predicted_revenue);
  resultModelInfo.textContent = `${model_type} — USD`;

  // Input summary table
  const labels = {
    marketing_spend:     'Marketing Spend',
    advertising_spend:   'Advertising Spend',
    website_traffic:     'Website Traffic',
    number_of_customers: 'Number of Customers',
    product_price:       'Product Price',
    discount_percentage: 'Discount Percentage',
    previous_revenue:    'Previous Revenue',
  };
  const formats = {
    marketing_spend:     v => formatCurrency(v),
    advertising_spend:   v => formatCurrency(v),
    website_traffic:     v => formatNumber(v),
    number_of_customers: v => formatNumber(v),
    product_price:       v => formatCurrency(v),
    discount_percentage: v => `${v.toFixed(1)}%`,
    previous_revenue:    v => formatCurrency(v),
  };

  inputSummaryBody.innerHTML = '';
  Object.entries(inputData).forEach(([key, value]) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${labels[key] || key}</td><td>${formats[key] ? formats[key](value) : value}</td>`;
    inputSummaryBody.appendChild(tr);
  });

  // Revenue comparison chart
  renderRevenueComparisonChart(inputData.previous_revenue, predicted_revenue);

  // Store for download
  lastPredictionResult = {
    timestamp:        new Date().toISOString(),
    model_name:       model,
    model_type:       model_type,
    input:            inputData,
    predicted_revenue,
    currency:         'USD',
  };
}

// ── Revenue comparison chart ──────────────────────────────────────────────────
function renderRevenueComparisonChart(previousRevenue, predictedRevenue) {
  const ctx = document.getElementById('chart-revenue-comparison');
  if (!ctx) return;

  // Destroy existing chart instance if present
  if (revenueComparisonChart) {
    revenueComparisonChart.destroy();
  }

  revenueComparisonChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Previous Revenue', 'Predicted Revenue'],
      datasets: [{
        label: 'Revenue (USD)',
        data: [previousRevenue, predictedRevenue],
        backgroundColor: [
          'rgba(217, 119, 6, 0.75)',
          'rgba(22, 163, 74, 0.75)',
        ],
        borderColor: [
          'rgba(217, 119, 6, 1)',
          'rgba(22, 163, 74, 1)',
        ],
        borderWidth: 1,
        borderRadius: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ` ${formatCurrency(ctx.raw)}`,
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: { callback: v => `$${(v / 1000).toFixed(0)}K` },
          beginAtZero: true,
        }
      }
    }
  });
}

// ── Download helpers ──────────────────────────────────────────────────────────

/**
 * Download prediction result as CSV.
 *
 * How browser download works:
 *   1. Create a Blob (binary large object) containing the file content
 *   2. Create a temporary <a> element with a download attribute
 *   3. Set the href to a temporary object URL for the Blob
 *   4. Programmatically click the <a> element to trigger the download
 *   5. Revoke the object URL to release memory
 *
 * This happens entirely in the browser — no server storage required.
 */
function downloadCSV() {
  if (!lastPredictionResult) return;

  const { timestamp, model_name, model_type, input, predicted_revenue, currency } = lastPredictionResult;

  const rows = [
    ['Field', 'Value'],
    ['Timestamp', timestamp],
    ['Model Name', model_name],
    ['Model Type', model_type],
    ['Currency', currency],
    ['', ''],
    ['--- Input Data ---', ''],
    ['Marketing Spend', input.marketing_spend],
    ['Advertising Spend', input.advertising_spend],
    ['Website Traffic', input.website_traffic],
    ['Number of Customers', input.number_of_customers],
    ['Product Price', input.product_price],
    ['Discount Percentage (%)', input.discount_percentage],
    ['Previous Revenue', input.previous_revenue],
    ['', ''],
    ['--- Prediction ---', ''],
    ['Predicted Revenue', predicted_revenue],
  ];

  const csvContent = rows.map(row => row.join(',')).join('\n');
  triggerDownload(csvContent, 'revenue_prediction.csv', 'text/csv');
}

function downloadJSON() {
  if (!lastPredictionResult) return;
  const content = JSON.stringify(lastPredictionResult, null, 2);
  triggerDownload(content, 'revenue_prediction.json', 'application/json');
}

function triggerDownload(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ── Form submit handler ───────────────────────────────────────────────────────
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  hideApiStatus();

  if (!validateForm()) return;

  const inputData = getFormValues();

  showLoading();

  try {
    const result = await predictRevenue(inputData);
    displayResult(result, inputData);
  } catch (error) {
    showApiStatus(
    `Unable to get prediction: ${error.message}. ` +
    'Please check the deployed backend API and try again.',
    'error'
    );
  } finally {
    hideLoading();
  }
});

// ── Reset button ──────────────────────────────────────────────────────────────
btnReset.addEventListener('click', () => {
  form.reset();
  Object.keys(VALIDATION_RULES).forEach(fieldId => {
    const input = document.getElementById(fieldId);
    const errorEl = document.getElementById(`err-${fieldId}`);
    if (input) input.classList.remove('error');
    if (errorEl) errorEl.classList.remove('visible');
  });
  hideApiStatus();
  resultPlaceholder.classList.remove('hidden');
  resultPanel.classList.add('hidden');
  lastPredictionResult = null;
  if (revenueComparisonChart) {
    revenueComparisonChart.destroy();
    revenueComparisonChart = null;
  }
});

// ── Download button handlers ──────────────────────────────────────────────────
btnDownloadCsv.addEventListener('click',  downloadCSV);
btnDownloadJson.addEventListener('click', downloadJSON);

// ── Backend connection check on page load ─────────────────────────────────────
// Checks whether the FastAPI backend is reachable when the prediction page loads.
// Shows a helpful status message — does not block the UI.
(async function checkBackendConnection() {
  try {
    await healthCheck();
    // Backend is up — show a subtle success confirmation
    showApiStatus('Backend API is connected and ready.', 'success');
    // Auto-hide after 4 seconds
    setTimeout(hideApiStatus, 4000);
  } catch (_) {
    showApiStatus(
      'Backend not reachable. Start the FastAPI server before making predictions: ' +
      'uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000',
      'error'
    );
    // Keep the error visible until the user resolves it
  }
})();
