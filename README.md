# Business Data Analysis and Revenue Prediction Platform

> **Capstone Design Project**
> IBM SkillsBuild University Education × Hacktiv8
> Course: Data — AI Agent for Data Analysis

An end-to-end Machine Learning web application that analyzes synthetic business data,
visualizes relationships between key business variables, and predicts revenue through
a REST API connected to an interactive frontend.

---

## Project Overview

This project demonstrates a complete, production-structured Machine Learning workflow —
from raw data generation through model training, REST API development, and a multi-page
web application with live prediction capabilities.

**What the application does:**

- Explores a 5,000-sample synthetic business revenue dataset through interactive charts
- Visualizes feature distributions, correlation analysis, and scatter plots
- Displays Linear Regression model performance (validation and test metrics)
- Accepts user business inputs and returns a live revenue prediction via FastAPI
- Allows users to download prediction results as CSV or JSON

---

## Technology Stack

| Layer | Technology |
|---|---|
| Data Analysis | Python, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | scikit-learn — Linear Regression, StandardScaler |
| Model Storage | joblib (local `.pkl` files) |
| Backend API | FastAPI, Uvicorn, Pydantic |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Frontend Charts | Chart.js 4.4 |
| Environment | Python 3.10, virtual environment |

---

## Machine Learning Pipeline

```
Dataset Generation (5,000 synthetic samples)
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Exploratory Data Analysis
        │
        ▼
StandardScaler (fit on training data only)
        │
        ▼
Train / Validation / Test Split  (70% / 15% / 15%)
        │
        ▼
Linear Regression Training
        │
        ▼
Validation Metrics  (R² = 0.8877)
        │
        ▼
Final Test Evaluation  (R² = 0.8847)
        │
        ▼
Model Saved  (models/)
        │
        ▼
FastAPI Backend  (POST /predict)
        │
        ▼
Web Application  (Prediction + Visualization)
```

---

## Model Performance

| Metric | Validation | Test |
|---|---|---|
| MAE | $14,128 | $14,127 |
| RMSE | $17,306 | $17,178 |
| R² Score | **0.8877** | **0.8847** |

- R² = 0.885 on the test set — the model explains **88.5% of revenue variance** on completely unseen data
- Validation vs Test R² gap = **0.003** — excellent generalisation, no overfitting
- Test set was isolated throughout development and used only once for final evaluation

---

## Dataset Features

| Feature | Description | Unit |
|---|---|---|
| `marketing_spend` | Marketing budget allocated | USD |
| `advertising_spend` | Advertising campaign cost | USD |
| `website_traffic` | Monthly website visitors | Count |
| `number_of_customers` | Customers in the period | Count |
| `product_price` | Average product price | USD |
| `discount_percentage` | Discount offered | % |
| `previous_revenue` | Revenue from prior period | USD |
| `revenue` | **Target variable** | USD |

Dataset: 5,000 synthetic samples with realistic business relationships and noise.
No real business data is used. The dataset is generated programmatically with a fixed
random seed for full reproducibility.

---

## Project Structure

```
business-revenue-platform/
│
├── data/
│   ├── raw/                    Raw generated dataset (CSV)
│   ├── processed/              Cleaned dataset
│   ├── train/                  Training split (70%)
│   ├── validation/             Validation split (15%)
│   └── test/                   Test split (15%) — isolated
│
├── data_generation/
│   └── generate_dataset.py     Synthetic dataset generator
│
├── notebooks/
│   ├── 01_data_analysis.ipynb      Exploratory Data Analysis
│   ├── 02_model_training.ipynb     Data preparation + model training
│   └── 03_model_evaluation.ipynb   Final evaluation + model saving
│
├── models/
│   ├── revenue_prediction_model.pkl  Trained Linear Regression
│   ├── preprocessing.pkl             Fitted StandardScaler
│   └── model_metadata.json           Metrics, features, versions
│
├── results/
│   └── visualizations/
│       ├── distributions/        Feature and revenue distribution plots
│       ├── correlation/          Correlation heatmap and bar chart
│       ├── scatter_plots/        Feature vs Revenue scatter plots
│       └── model_evaluation/     Actual vs Predicted, residuals, coefficients
│
├── backend/
│   ├── main.py                   FastAPI application, CORS, endpoints
│   ├── config/settings.py        Path and API configuration
│   ├── schemas/prediction.py     Pydantic request/response models
│   ├── services/model_loader.py  Model artifact loading (startup)
│   ├── services/predictor.py     Prediction pipeline
│   └── requirements.txt
│
├── frontend/
│   ├── index.html                Home page
│   ├── dashboard.html            Data Analysis Dashboard
│   ├── model.html                Model Performance
│   ├── prediction.html           Revenue Prediction
│   ├── css/style.css             Shared stylesheet
│   └── js/
│       ├── api.js                Backend API service layer
│       ├── main.js               Shared utilities
│       ├── dashboard.js          Dashboard Chart.js charts
│       ├── model.js              Model metrics + live API fetch
│       └── prediction.js         Form, prediction, download
│
├── requirements.txt              Root dependencies (notebooks, data scripts)
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/business-revenue-platform.git
cd business-revenue-platform
```

### 2. Create and activate a virtual environment

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
# Root dependencies (notebooks, data scripts)
pip install -r requirements.txt

# Backend dependencies
pip install -r backend/requirements.txt
```

### 4. Generate the dataset

```bash
python data_generation/generate_dataset.py
```

Output: `data/raw/business_revenue_dataset.csv` (5,000 samples)

### 5. Run the Jupyter notebooks

Register the virtual environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name=venv_revenue --display-name="Python (revenue-platform)"
jupyter notebook
```

Run in order:
1. `notebooks/01_data_analysis.ipynb` — EDA and visualizations
2. `notebooks/02_model_training.ipynb` — Data preparation and model training
3. `notebooks/03_model_evaluation.ipynb` — Final evaluation and model saving

> **Note:** The trained model files (`models/`) are included in the repository.
> You can skip the notebooks and proceed directly to running the backend.

### 6. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

- API base URL: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs

### 7. Open the frontend

Open `frontend/index.html` with VS Code Live Server, or serve with any static file server:

```bash
# Using Python's built-in server (from the frontend/ directory)
cd frontend
python -m http.server 5500
```

Then open: http://127.0.0.1:5500

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/model-info` | Model metadata and performance metrics |
| `POST` | `/predict` | Revenue prediction |

### Example: POST /predict

**Request:**
```json
{
  "marketing_spend": 10000,
  "advertising_spend": 5000,
  "website_traffic": 50000,
  "number_of_customers": 1200,
  "product_price": 50,
  "discount_percentage": 10,
  "previous_revenue": 100000
}
```

**Response:**
```json
{
  "predicted_revenue": 80664.86,
  "currency": "USD",
  "model": "Business Revenue Prediction Model",
  "model_type": "Linear Regression"
}
```

**Validation rules:**
- All fields required
- `marketing_spend`, `advertising_spend`, `website_traffic`, `number_of_customers`, `previous_revenue` ≥ 0
- `product_price` > 0
- `discount_percentage` between 0 and 100

---

## Frontend Pages

| Page | File | Description |
|---|---|---|
| Home | `index.html` | Project overview, ML workflow, tech stack, navigation |
| Data Analysis | `dashboard.html` | EDA dashboard — statistics, distributions, correlations, scatter plots |
| Model Performance | `model.html` | Validation/test metrics, R² explanation, feature coefficients |
| Prediction | `prediction.html` | Prediction form, result display, comparison chart, download |

---

## Key Design Decisions

**Why StandardScaler for Linear Regression?**
Scaling does not change prediction accuracy for OLS regression, but it makes
coefficients directly comparable across features and ensures the backend pipeline
correctly processes user inputs in the same numerical space as training data.

**Why isolate the test set?**
The test set was set aside at the beginning and used exactly once — for the final
evaluation in `03_model_evaluation.ipynb`. This produces an honest, unbiased
performance estimate that was not influenced by any model or preprocessing decisions.

**Why load the model at startup?**
Loading `.pkl` files involves disk I/O on every request if done per-request.
FastAPI's lifespan context manager loads the model once at startup, keeping it
in memory for the lifetime of the server — standard practice for ML serving.

**Why vanilla HTML/CSS/JavaScript?**
The frontend was intentionally built without frameworks to demonstrate fundamental
web development skills — DOM manipulation, fetch API, event handling, and
Chart.js integration — all without abstraction layers.

---

## Results & Visualizations

All EDA and model evaluation visualizations are saved in `results/visualizations/`:

| Visualization | File |
|---|---|
| Feature distributions | `distributions/feature_distributions.png` |
| Feature box plots | `distributions/feature_boxplots.png` |
| Revenue distribution | `distributions/revenue_distribution.png` |
| Correlation heatmap | `correlation/correlation_heatmap.png` |
| Feature correlations with revenue | `correlation/revenue_correlations.png` |
| All features vs Revenue scatter | `scatter_plots/features_vs_revenue.png` |
| Previous Revenue vs Revenue | `scatter_plots/previous_revenue_vs_revenue.png` |
| Actual vs Predicted | `model_evaluation/actual_vs_predicted.png` |
| Residual analysis | `model_evaluation/residual_analysis.png` |
| Feature coefficients | `model_evaluation/feature_coefficients.png` |

---

## Development Status

| Phase | Description | Status |
|---|---|---|
| 1 | Project Setup | Complete |
| 2 | Synthetic Dataset Generation | Complete |
| 3 | Exploratory Data Analysis | Complete |
| 4 | Data Preparation & Feature Engineering | Complete |
| 5 | Model Training | Complete |
| 6 | Model Evaluation & Saving | Complete |
| 7 | FastAPI Backend | Complete |
| 8 | Frontend Development | Complete |
| 9 | Frontend & Backend Integration | Complete |
| 10 | Final Review & Documentation | Complete |

**Planned future phases:**
- Hugging Face Hub model storage and deployment
- Cloud backend deployment
- Vercel frontend deployment
- Docker containerization

---

## License

For educational and portfolio purposes.
IBM SkillsBuild University Education × Hacktiv8 Capstone Design Project.
