/**
 * api.js
 * ------
 * API service layer — all HTTP communication with the FastAPI backend.
 *
 * This file is the single place where the frontend talks to the backend.
 * No other JavaScript file should make fetch() calls directly.
 *
 * Base URL points to the local FastAPI backend.
 * Full implementation is wired in Phase 9.
 */

'use strict';

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * GET /health
 * Check whether the backend API is running.
 * @returns {Promise<Object>} { status, service, version }
 */
async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error(`Health check failed: ${response.status}`);
  return response.json();
}

/**
 * GET /model-info
 * Retrieve model metadata and performance metrics.
 * @returns {Promise<Object>} model info object
 */
async function getModelInfo() {
  const response = await fetch(`${API_BASE_URL}/model-info`);
  if (!response.ok) throw new Error(`Model info request failed: ${response.status}`);
  return response.json();
}

/**
 * POST /predict
 * Send business input data and receive a revenue prediction.
 *
 * @param {Object} inputData - The 7 business input features
 * @param {number} inputData.marketing_spend
 * @param {number} inputData.advertising_spend
 * @param {number} inputData.website_traffic
 * @param {number} inputData.number_of_customers
 * @param {number} inputData.product_price
 * @param {number} inputData.discount_percentage
 * @param {number} inputData.previous_revenue
 *
 * @returns {Promise<Object>} { predicted_revenue, currency, model, model_type }
 */
async function predictRevenue(inputData) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(inputData),
  });

  if (!response.ok) {
    // Try to extract the FastAPI error detail
    let detail = `Prediction request failed (HTTP ${response.status})`;
    try {
      const errorBody = await response.json();
      if (errorBody.detail) {
        detail = typeof errorBody.detail === 'string'
          ? errorBody.detail
          : JSON.stringify(errorBody.detail);
      }
    } catch (_) { /* ignore JSON parse errors */ }
    throw new Error(detail);
  }

  return response.json();
}
