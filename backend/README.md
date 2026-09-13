# Backend — Revenue Prediction API

FastAPI backend for the Business Data Analysis and Revenue Prediction Platform.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/model-info` | Model metadata and performance metrics |
| `POST` | `/predict` | Revenue prediction |

Interactive API docs: http://127.0.0.1:8000/docs

---

## Running the Backend

From the **project root** directory (not inside `backend/`):

```bash
# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Start the server
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

The `--reload` flag restarts the server automatically when code changes.
Remove it in production.

---

## Project Structure

```
backend/
├── main.py                   FastAPI app — CORS, lifespan, endpoints
├── config/
│   └── settings.py           Paths, API title, CORS origins
├── schemas/
│   └── prediction.py         PredictionRequest, PredictionResponse, HealthResponse
├── services/
│   ├── model_loader.py       Loads model artifacts at application startup
│   └── predictor.py          Input → DataFrame → scale → predict → float
└── requirements.txt
```

---

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "marketing_spend": 10000,
    "advertising_spend": 5000,
    "website_traffic": 50000,
    "number_of_customers": 1200,
    "product_price": 50,
    "discount_percentage": 10,
    "previous_revenue": 100000
  }'
```

Expected response:
```json
{
  "predicted_revenue": 80664.86,
  "currency": "USD",
  "model": "Business Revenue Prediction Model",
  "model_type": "Linear Regression"
}
```

---

## Input Validation

| Field | Rule |
|---|---|
| `marketing_spend` | >= 0 |
| `advertising_spend` | >= 0 |
| `website_traffic` | >= 0 |
| `number_of_customers` | >= 0 |
| `product_price` | > 0 |
| `discount_percentage` | 0 to 100 |
| `previous_revenue` | >= 0 |

Invalid input returns HTTP **422 Unprocessable Entity** with a detailed error message.

---

## Requirements

```bash
pip install -r requirements.txt
```

Dependencies: `fastapi`, `uvicorn[standard]`, `pydantic`, `scikit-learn`, `numpy`, `pandas`, `joblib`

---

## Prerequisites

The model artifacts must exist in `models/` before starting the server:
- `models/revenue_prediction_model.pkl`
- `models/preprocessing.pkl`
- `models/model_metadata.json`

Run `notebooks/03_model_evaluation.ipynb` to generate them.
