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

from fastapi import FastAPI
from fastapi import HTTPException

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


from backend.services.model_loader import (

    model_loader,

)


from backend.services.predictor import (

    predict_revenue,

)


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(

    title=API_TITLE,

    description=API_DESCRIPTION,

    version=API_VERSION,

)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=CORS_ORIGINS,

    allow_credentials=False,

    allow_methods=["GET", "POST"],

    allow_headers=["Content-Type"],

)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Model Info
# ---------------------------------------------------------

@app.get(

    "/api/model-info",

    summary="Model information",

    tags=["Model"],

)

async def model_info():

    # Load model only when needed
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


# ---------------------------------------------------------
# Prediction
# ---------------------------------------------------------

@app.post(

    "/api/predict",

    response_model=PredictionResponse,

    summary="Predict revenue",

    tags=["Prediction"],

)

async def predict(

    request: PredictionRequest

):


    # Load model if necessary
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

        predicted_revenue=

            predicted_revenue,


        currency=

            "USD",


        model=

            model_loader.model_name,


        model_type=

            model_loader.model_type,

    )