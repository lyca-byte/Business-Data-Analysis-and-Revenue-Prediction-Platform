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

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


# ── Lifespan: load model at startup ──────────────────────────────────────────
# FastAPI's lifespan context manager replaces the old @app.on_event("startup").
# Code before `yield` runs at startup; code after `yield` runs at shutdown.
# Loading the model here means it is ready before the first request arrives.

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        model_loader.load()
        print(f"[startup] Model loaded: {model_loader.model_name}")
        print(f"[startup] Features    : {model_loader.feature_columns}")
    except FileNotFoundError as e:
        print(f"[startup] ERROR: Model artifact not found — {e}")
        print("[startup] Run the training notebook first to generate model files.")
        raise
    yield
    # Shutdown (nothing to clean up for this project)
    print("[shutdown] Application stopping.")


# ── FastAPI application ───────────────────────────────────────────────────────
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
)


# ── CORS middleware ───────────────────────────────────────────────────────────
# CORS (Cross-Origin Resource Sharing) controls which origins can make
# HTTP requests to this API from a browser.
#
# Why it is necessary:
#   Browsers enforce the Same-Origin Policy — a web page can only make
#   requests to the same origin (host + port) it was loaded from.
#   Our frontend runs on port 5500 (VS Code Live Server) and the backend
#   runs on port 8000. Without CORS headers, the browser blocks the request.
#
# allow_credentials=False is correct here because we are not using
# cookies or authentication tokens.

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ── Endpoint 1: Health Check ──────────────────────────────────────────────────
@app.get(
    "/api/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["System"],
)
async def health_check():
    """
    Returns the current health status of the API.

    Use this to verify the backend is running before making prediction requests.
    """
    return HealthResponse(
        status="healthy",
        service=API_TITLE,
        version=API_VERSION,
    )


# ── Endpoint 2: Model Information ─────────────────────────────────────────────
@app.get(
    "/api/model-info",
    summary="Model information and performance metrics",
    tags=["Model"],
)
async def model_info():
    """
    Returns metadata about the trained model including:
    - Model name and type
    - Input features
    - Validation and test performance metrics
    - Training date and library versions
    """
    if not model_loader.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    meta = model_loader.metadata

    return {
        "model_name":    meta["model_name"],
        "model_type":    meta["model_type"],
        "target":        meta["target"],
        "features":      meta["features"],
        "feature_count": meta["feature_count"],
        "training_date": meta["training_date"],
        "dataset": {
            "total_samples":      meta["dataset"]["total_samples"],
            "train_samples":      meta["dataset"]["train_samples"],
            "validation_samples": meta["dataset"]["validation_samples"],
            "test_samples":       meta["dataset"]["test_samples"],
        },
        "validation_metrics": meta["validation_metrics"],
        "test_metrics":       meta["test_metrics"],
        "library_versions":   meta["library_versions"],
    }


# ── Endpoint 3: Revenue Prediction ────────────────────────────────────────────
@app.post(
    "/api/predict",
    response_model=PredictionResponse,
    summary="Predict revenue from business inputs",
    tags=["Prediction"],
)
async def predict(request: PredictionRequest):
    """
    Accepts 7 business input features and returns a predicted revenue.

    **Input validation rules:**
    - `marketing_spend` >= 0
    - `advertising_spend` >= 0
    - `website_traffic` >= 0
    - `number_of_customers` >= 0
    - `product_price` > 0
    - `discount_percentage` between 0 and 100
    - `previous_revenue` >= 0

    Returns the predicted revenue in USD.
    """
    if not model_loader.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    try:
        predicted_revenue = predict_revenue(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )

    return PredictionResponse(
        predicted_revenue=predicted_revenue,
        currency="USD",
        model=model_loader.model_name,
        model_type=model_loader.model_type,
    )
