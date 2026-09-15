"""
settings.py
-----------
Central configuration for the Revenue Prediction API backend.

All file paths are defined here so that no other file needs to
hardcode directory locations. If the project folder moves, only
this file needs to change.
"""

import os


# ---------------------------------------------------------
# Hugging Face Configuration
# ---------------------------------------------------------

HF_REPO_ID = os.getenv("HF_REPO_ID","").strip()

HF_TOKEN = os.getenv("HF_TOKEN","").strip()

# ---------------------------------------------------------
# Validate Repository
# ---------------------------------------------------------
if not HF_REPO_ID:
    print("[config] WARNING: ""HF_REPO_ID is not configured.")

print(f"[config] HF_REPO_ID: " f"{HF_REPO_ID}")

print(
    f"[config] HF_TOKEN configured: "
    f"{bool(HF_TOKEN)}"
)


# ---------------------------------------------------------
# API Configuration
# ---------------------------------------------------------

API_TITLE = (

    "Business Revenue Prediction API"

)


API_DESCRIPTION = (

    "REST API for the Business Data Analysis "
    "and Revenue Prediction Platform. "
    "Provides revenue prediction using "
    "a trained Linear Regression model."

)


API_VERSION = "1.0.0"


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

CORS_ORIGINS = [

    "http://127.0.0.1:5500",

    "http://localhost:5500",

    "http://127.0.0.1:5501",

    "http://localhost:5501",

    "http://127.0.0.1:3000",

    "http://localhost:3000",

]