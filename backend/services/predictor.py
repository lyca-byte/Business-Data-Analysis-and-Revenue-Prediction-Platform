"""
predictor.py
------------
Prediction service for the Revenue Prediction API.

Receives a validated PredictionRequest, prepares the data,
applies preprocessing, runs the model, and returns a result dict.

The API route in main.py delegates all ML logic here so that
main.py stays clean and focused on HTTP concerns only.

Prediction workflow:
    PredictionRequest (validated Pydantic model)
        │
        ▼
    Convert to pandas DataFrame with correct feature order
        │
        ▼
    StandardScaler transform (using the fitted scaler from training)
        │
        ▼
    LinearRegression predict
        │
        ▼
    Return predicted revenue (float)
"""

import pandas as pd
import numpy as np

from backend.schemas.prediction import PredictionRequest
from backend.services.model_loader import model_loader


def predict_revenue(request: PredictionRequest) -> float:
    """
    Generate a revenue prediction from a validated PredictionRequest.

    Args:
        request: Validated PredictionRequest Pydantic model.

    Returns:
        Predicted revenue as a float (USD).

    Raises:
        RuntimeError: If the model has not been loaded.
    """
    if not model_loader.is_loaded:
        raise RuntimeError("Model is not loaded. Cannot generate prediction.")

    # ── Step 1: Build a DataFrame with the correct feature order ──────────────
    # Feature order MUST match exactly what the model was trained on.
    # model_loader.feature_columns comes from model_metadata.json,
    # which was written during training — the single source of truth.
    input_data = pd.DataFrame(
        [[
            request.marketing_spend,
            request.advertising_spend,
            request.website_traffic,
            request.number_of_customers,
            request.product_price,
            request.discount_percentage,
            request.previous_revenue,
        ]],
        columns=model_loader.feature_columns,
    )

    # ── Step 2: Apply the fitted StandardScaler ───────────────────────────────
    # We apply the SAME scaler that was fitted on the training data.
    # This ensures the model receives data in the same numerical range
    # it learned from. Never fit a new scaler on incoming prediction data.
    input_scaled = model_loader.scaler.transform(input_data)

    # ── Step 3: Generate prediction ───────────────────────────────────────────
    prediction = model_loader.model.predict(input_scaled)

    # prediction is a numpy array with one element; extract the float value
    predicted_revenue = float(prediction[0])

    # Clip to a sensible minimum — the model should not predict negative revenue
    predicted_revenue = max(predicted_revenue, 0.0)

    return round(predicted_revenue, 2)
