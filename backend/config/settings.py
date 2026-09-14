"""
settings.py
-----------
Central configuration for the Revenue Prediction API backend.

All file paths are defined here so that no other file needs to
hardcode directory locations. If the project folder moves, only
this file needs to change.
"""

import os

# Config for Hugging Face
HF_REPO_ID = os.getenv(
    "HF_REPO_ID",
    "lyca-byte/business-revenue-prediction-model"
)

HF_TOKEN = os.getenv(
    "HF_TOKEN"
)

# ── Base directory ────────────────────────────────────────────────────────────
# __file__ is backend/config/settings.py
# We go up two levels to reach the project root.
_CONFIG_DIR  = os.path.dirname(os.path.abspath(__file__))   # backend/config/
_BACKEND_DIR = os.path.dirname(_CONFIG_DIR)                  # backend/
PROJECT_ROOT = os.path.dirname(_BACKEND_DIR)                 # project root/

# ── Model artifact paths ──────────────────────────────────────────────────────
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

MODEL_PATH    = os.path.join(MODELS_DIR, "revenue_prediction_model.pkl")
SCALER_PATH   = os.path.join(MODELS_DIR, "preprocessing.pkl")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

# ── API configuration ─────────────────────────────────────────────────────────
API_TITLE       = "Business Revenue Prediction API"
API_DESCRIPTION = (
    "REST API for the Business Data Analysis and Revenue Prediction Platform. "
    "Provides revenue prediction using a trained Linear Regression model."
)
API_VERSION = "1.0.0"

# ── CORS origins ──────────────────────────────────────────────────────────────
# These are the frontend origins allowed to call the API during local development.
# Both 127.0.0.1 and localhost variants are included because browsers treat
# them differently — some tools default to one or the other.
CORS_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
