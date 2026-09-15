"""
main.py
-------
FastAPI application entry point for the Revenue Prediction API.

Endpoints:
    GET  /health      -- health check
    GET  /model-info  -- model metadata and performance metrics
    POST /predict     -- revenue prediction

Run with:
    uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

Or from inside the backend/ directory:
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
"""
"""
main.py
-------
FastAPI application entry point.
"""

"""
main.py
-------
FastAPI application for the Business Data Analysis
and Revenue Prediction Platform.
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.config.settings import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    CORS_ORIGINS,
)

from backend.schemas.prediction import (
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
)

from backend.services.model_loader import model_loader
from backend.services.predictor import predict_revenue


# =========================================================
# Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# =========================================================
# Frontend Pages
# =========================================================

@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/index.html", include_in_schema=False)
async def index_page():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/dashboard.html", include_in_schema=False)
async def dashboard_page():
    return FileResponse(
        FRONTEND_DIR / "dashboard.html"
    )


@app.get("/model.html", include_in_schema=False)
async def model_page():
    return FileResponse(
        FRONTEND_DIR / "model.html"
    )


@app.get("/prediction.html", include_in_schema=False)
async def prediction_page():
    return FileResponse(
        FRONTEND_DIR / "prediction.html"
    )


# =========================================================
# Frontend CSS
# =========================================================

@app.get("/css/{filename}", include_in_schema=False)
async def css_file(filename: str):

    file_path = FRONTEND_DIR / "css" / filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="CSS file not found",
        )

    return FileResponse(file_path)


# =========================================================
# Frontend JavaScript
# =========================================================

@app.get("/js/{filename}", include_in_schema=False)
async def javascript_file(filename: str):

    file_path = FRONTEND_DIR / "js" / filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="JavaScript file not found",
        )

    return FileResponse(file_path)


# =========================================================
# API Health Check
# =========================================================

@app.get(
    "/api/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["System"],
)
async def health_check():

    return HealthResponse(
        status="healthy",
        service=API_TITLE,
        version=API_VERSION,
    )


# =========================================================
# Debug Configuration
# =========================================================

@app.get(
    "/api/debug-config",
    include_in_schema=False,
)
async def debug_config():

    return {
        "hf_repo_id": os.getenv("HF_REPO_ID"),
        "hf_token_configured": bool(
            os.getenv("HF_TOKEN")
        ),
        "hf_home": os.getenv("HF_HOME"),
        "hf_hub_cache": os.getenv("HF_HUB_CACHE"),
        "frontend_exists": FRONTEND_DIR.exists(),
        "frontend_path": str(FRONTEND_DIR),
    }


# =========================================================
# Model Information
# =========================================================

@app.get(
    "/api/model-info",
    summary="Model information",
    tags=["Model"],
)
async def model_info():

    success = model_loader.ensure_loaded()

    if not success:

        raise HTTPException(
            status_code=503,
            detail={
                "message":
                    "Model could not be loaded.",
                "error":
                    model_loader.load_error,
            },
        )

    meta = model_loader.metadata

    return {
        "model_name":
            meta["model_name"],

        "model_type":
            meta["model_type"],

        "target":
            meta["target"],

        "features":
            meta["features"],

        "feature_count":
            meta["feature_count"],

        "training_date":
            meta["training_date"],

        "dataset":
            meta["dataset"],

        "validation_metrics":
            meta["validation_metrics"],

        "test_metrics":
            meta["test_metrics"],

        "library_versions":
            meta["library_versions"],
    }


# =========================================================
# Revenue Prediction
# =========================================================

@app.post(
    "/api/predict",
    response_model=PredictionResponse,
    summary="Predict revenue",
    tags=["Prediction"],
)
async def predict(
    request: PredictionRequest,
):

    success = model_loader.ensure_loaded()

    if not success:

        raise HTTPException(
            status_code=503,
            detail={
                "message":
                    "Model could not be loaded.",
                "error":
                    model_loader.load_error,
            },
        )

    try:

        predicted_revenue = predict_revenue(
            request
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Prediction failed.",
                "error":
                    str(e),
            },
        )

    return PredictionResponse(
        predicted_revenue=predicted_revenue,
        currency="USD",
        model=model_loader.model_name,
        model_type=model_loader.model_type,
    )