# Business Data Analysis and Revenue Prediction Platform

> **Capstone Design Project**  
> IBM SkillsBuild University Education × Hacktiv8
> Course: Data — AI Agent for Data Analysis

An end-to-end Machine Learning web application for business data analysis and revenue prediction. The platform combines synthetic business data generation, exploratory data analysis, Linear Regression modeling, REST API development, and an interactive web-based frontend.

The application allows users to explore business data, review model performance, and generate revenue predictions by entering business-related input variables.

## Live Application

Production deployment:

> https://business-data-analysis-and-revenue.vercel.app

The application is deployed on Vercel with a FastAPI backend and a static HTML, CSS, and JavaScript frontend.

---

## Project Overview

This project demonstrates an end-to-end Machine Learning workflow, from synthetic dataset generation and exploratory analysis to model training, evaluation, API integration, and cloud deployment.

The platform provides three main functions:

* Analyze and visualize synthetic business data
* Display Linear Regression model performance and evaluation metrics
* Generate revenue predictions from user-provided business inputs

The application uses a trained Linear Regression model with StandardScaler preprocessing. The production backend retrieves the trained model artifacts from Hugging Face Hub and serves predictions through FastAPI.

No real business or customer data is used in this project.

---

## Main Features

### 1. Business Data Analysis

The Data Analysis Dashboard provides visual exploration of the generated business dataset, including:

* Feature statistics
* Feature distributions
* Revenue distribution
* Correlation analysis
* Feature-to-revenue relationships
* Interactive charts using Chart.js

### 2. Model Performance

The Model Performance page displays:

* Validation MAE
* Validation RMSE
* Validation R²
* Test MAE
* Test RMSE
* Test R²
* Feature coefficients
* Model information

The page retrieves model information from the deployed backend API when the API is available.

### 3. Revenue Prediction

The Prediction page provides an interactive form for seven business input variables:

* Marketing Spend
* Advertising Spend
* Website Traffic
* Number of Customers
* Product Price
* Discount Percentage
* Previous Revenue

The submitted values are sent to the FastAPI backend, processed using the same preprocessing pipeline used during training, and passed to the trained Linear Regression model.

The resulting predicted revenue is displayed directly in the web application.

### 4. Prediction Result Download

Prediction results can be downloaded from the frontend in supported formats such as:

* CSV
* JSON

---

## Technology Stack

| Layer                   | Technology                                   |
| ----------------------- | -------------------------------------------- |
| Programming Language    | Python                                       |
| Data Processing         | Pandas, NumPy                                |
| Data Visualization      | Matplotlib, Seaborn                          |
| Machine Learning        | scikit-learn                                 |
| ML Algorithm            | Linear Regression                            |
| Preprocessing           | StandardScaler                               |
| Model Serialization     | joblib                                       |
| Backend API             | FastAPI                                      |
| API Validation          | Pydantic                                     |
| Local Server            | Uvicorn                                      |
| Frontend                | HTML5, CSS3, Vanilla JavaScript              |
| Frontend Visualization  | Chart.js                                     |
| Model Hosting           | Hugging Face Hub                             |
| Web Deployment          | Vercel                                       |
| Development Environment | Python virtual environment, Jupyter Notebook |

---

## Machine Learning Pipeline

```text
Synthetic Business Dataset
        |
        v
Data Cleaning and Validation
        |
        v
Exploratory Data Analysis
        |
        v
Train / Validation / Test Split
        |
        +-----------------------------+
        |                             |
        v                             |
StandardScaler                        |
        |                             |
        v                             |
Linear Regression Training            |
        |                             |
        v                             |
Validation Evaluation                 |
        |                             |
        v                             |
Final Test Evaluation <---------------+
        |
        v
Model and Preprocessing Artifacts
        |
        +--------------------+
        |                    |
        v                    v
Hugging Face Hub        Local Development
        |
        v
FastAPI Backend
        |
        v
/api/model-info
/api/predict
        |
        v
Web Application
```

---

## Model Performance

The current trained model uses Linear Regression with StandardScaler preprocessing.

| Metric   | Validation |       Test |
| -------- | ---------: | ---------: |
| MAE      |    $14,128 |    $14,127 |
| RMSE     |    $17,306 |    $17,178 |
| R² Score | **0.8877** | **0.8847** |

The test R² score of approximately 0.885 indicates that the model explains approximately 88.5% of the variance in revenue on the held-out test set.

The validation and test R² scores are close to each other, with a difference of approximately 0.003. This indicates consistent performance between the validation and test sets for this synthetic dataset.

The test set is kept isolated from model development and is used for final evaluation.

---

## Dataset

The project uses a programmatically generated synthetic business revenue dataset containing 5,000 samples.

The dataset is designed to represent relationships between business spending, customer activity, pricing, discounts, previous revenue, and current revenue.

### Dataset Features

| Feature               | Description                                       | Unit  |
| --------------------- | ------------------------------------------------- | ----- |
| `marketing_spend`     | Marketing budget allocated to business activities | USD   |
| `advertising_spend`   | Advertising and campaign expenditure              | USD   |
| `website_traffic`     | Number of website visitors                        | Count |
| `number_of_customers` | Number of customers during the period             | Count |
| `product_price`       | Average product price                             | USD   |
| `discount_percentage` | Discount percentage offered                       | %     |
| `previous_revenue`    | Revenue from the previous period                  | USD   |
| `revenue`             | Target variable representing current revenue      | USD   |

The dataset does not contain real customer, company, or financial information.

---

## Model Artifacts

The production application uses three model-related artifacts:

```text
revenue_prediction_model.pkl
preprocessing.pkl
model_metadata.json
```

These files are hosted in the project's public Hugging Face repository:

```text
lyca-byte/business-revenue-prediction-model
```

The backend retrieves the artifacts from Hugging Face Hub when required.

### Artifact Description

| Artifact                       | Purpose                                                     |
| ------------------------------ | ----------------------------------------------------------- |
| `revenue_prediction_model.pkl` | Trained Linear Regression model                             |
| `preprocessing.pkl`            | Fitted StandardScaler                                       |
| `model_metadata.json`          | Model information, features, metrics, and training metadata |

For local development, the artifacts can also be stored in the project's `models/` directory when available.

---

## Production Architecture

The deployed application uses the following architecture:

```text
                         User Browser
                              |
                              v
              +-----------------------------+
              |        Vercel Deployment    |
              |                             |
              |  Frontend                   |
              |  HTML / CSS / JavaScript    |
              |                             |
              |  FastAPI Serverless API     |
              +--------------+--------------+
                             |
                             | /api/*
                             v
                  +----------------------+
                  |     FastAPI API      |
                  |                      |
                  | /api/health          |
                  | /api/model-info      |
                  | /api/predict         |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |   Hugging Face Hub   |
                  |                      |
                  | Model                |
                  | Preprocessing        |
                  | Metadata             |
                  +----------------------+
```

The frontend and backend communicate through same-origin `/api` requests in production.

---

## Project Structure

```text
business-data-analysis-and-revenue-prediction-platform/
|
├── api/
│   └── index.py                  Vercel FastAPI entry point
|
├── backend/
│   ├── config/
│   │   └── settings.py           Backend configuration
│   │
│   ├── schemas/
│   │   └── prediction.py         Pydantic request/response schemas
│   │
│   ├── services/
│   │   ├── model_loader.py       Model artifact loading
│   │   └── predictor.py          Prediction pipeline
│   │
│   ├── main.py                   FastAPI application and routes
│   └── requirements.txt          Backend dependencies
|
├── data/
│   ├── raw/                      Generated raw dataset
│   ├── processed/                Processed dataset
│   ├── train/                    Training data
│   ├── validation/              Validation data
│   └── test/                     Test data
|
├── data_generation/
│   └── generate_dataset.py       Synthetic dataset generator
|
├── frontend/
│   ├── index.html                Home page
│   ├── dashboard.html            Data Analysis Dashboard
│   ├── model.html                Model Performance
│   ├── prediction.html           Revenue Prediction
│   │
│   ├── css/
│   │   └── style.css             Shared stylesheet
│   │
│   └── js/
│       ├── api.js                API communication
│       ├── main.js               Shared frontend utilities
│       ├── dashboard.js          Dashboard visualizations
│       ├── model.js              Model information and metrics
│       └── prediction.js         Prediction form and results
|
├── models/
│   ├── revenue_prediction_model.pkl
│   ├── preprocessing.pkl
│   └── model_metadata.json
|
├── notebooks/
│   ├── 01_data_analysis.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_model_evaluation.ipynb
|
├── results/
│   └── visualizations/
│       ├── distributions/
│       ├── correlation/
│       ├── scatter_plots/
│       └── model_evaluation/
|
├── .gitignore
├── .vercelignore
├── requirements.txt
├── vercel.json
└── README.md
```

---

## Getting Started

### Prerequisites

* Python 3.10 or newer
* pip
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/business-data-analysis-and-revenue-prediction-platform.git
cd business-data-analysis-and-revenue-prediction-platform
```

### 2. Create a Virtual Environment

#### Windows PowerShell

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For backend-specific development:

```bash
pip install -r backend/requirements.txt
```

---

## Generate the Dataset

The synthetic dataset can be regenerated using:

```bash
python data_generation/generate_dataset.py
```

The generated dataset is used for analysis and model development.

---

## Model Development

The notebooks are designed to be executed in sequence:

```text
01_data_analysis.ipynb
        |
        v
02_model_training.ipynb
        |
        v
03_model_evaluation.ipynb
```

### Notebook 1 — Data Analysis

Performs:

* Dataset inspection
* Data quality checks
* Descriptive statistics
* Feature distributions
* Correlation analysis
* Exploratory visualizations

### Notebook 2 — Model Training

Performs:

* Data preparation
* Train / validation / test split
* StandardScaler fitting
* Linear Regression training
* Validation evaluation
* Model artifact saving

### Notebook 3 — Model Evaluation

Performs:

* Final test evaluation
* Actual vs predicted analysis
* Residual analysis
* Feature coefficient analysis
* Model metadata generation

---

## Running the Backend Locally

Start the FastAPI server using:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

The local API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

The backend requires the Hugging Face repository configuration when using the production model-loading workflow.

Example environment variables:

```text
HF_REPO_ID=lyca-byte/business-revenue-prediction-model
HF_TOKEN=<your-hugging-face-token>
```

For a public Hugging Face repository, authentication may not be required for downloading public artifacts, but the application supports `HF_TOKEN` when configured.

---

## Running the Frontend Locally

The frontend consists of static HTML, CSS, and JavaScript files.

From the `frontend/` directory:

```bash
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

For local development, the frontend communicates with the FastAPI backend through the configured API base URL.

In production, the frontend uses the same-origin API path:

```text
/api
```

---

## API Endpoints

The production API is available under the `/api` path.

| Method | Endpoint          | Description                            |
| ------ | ----------------- | -------------------------------------- |
| `GET`  | `/api/health`     | API health check                       |
| `GET`  | `/api/model-info` | Model metadata and performance metrics |
| `POST` | `/api/predict`    | Generate revenue prediction            |

### Health Check

```text
GET /api/health
```

Example response:

```json
{
  "status": "healthy",
  "service": "Business Revenue Prediction API",
  "version": "1.0.0"
}
```

### Model Information

```text
GET /api/model-info
```

This endpoint provides information such as:

* Model name
* Model type
* Target variable
* Input features
* Dataset information
* Validation metrics
* Test metrics
* Training metadata
* Library versions

### Revenue Prediction

```text
POST /api/predict
```

Example request:

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

Example response:

```json
{
  "predicted_revenue": 80664.86,
  "currency": "USD",
  "model": "Business Revenue Prediction Model",
  "model_type": "Linear Regression"
}
```

### Input Validation

The API validates all prediction inputs using Pydantic.

Validation rules include:

* `marketing_spend` must be greater than or equal to 0
* `advertising_spend` must be greater than or equal to 0
* `website_traffic` must be greater than or equal to 0
* `number_of_customers` must be greater than or equal to 0
* `product_price` must be greater than 0
* `discount_percentage` must be between 0 and 100
* `previous_revenue` must be greater than or equal to 0

---

## Frontend Pages

| Page              | Description                              |
| ----------------- | ---------------------------------------- |
| `index.html`      | Project overview and navigation          |
| `dashboard.html`  | Business data analysis dashboard         |
| `model.html`      | Model performance and evaluation metrics |
| `prediction.html` | Revenue prediction interface             |

### Home

Provides an overview of the project, Machine Learning workflow, and application features.

### Data Analysis

Provides visual analysis of the synthetic business dataset.

### Model Performance

Displays model evaluation results and retrieves model information from the backend API.

### Prediction

Provides a user-friendly form for submitting business variables and obtaining a predicted revenue value from the deployed Machine Learning model.

---

## Deployment

The production application is deployed using Vercel.

The deployment consists of:

```text
frontend/
    |
    +-- Static HTML
    +-- CSS
    +-- JavaScript

api/index.py
    |
    v
FastAPI
    |
    v
Hugging Face Hub
    |
    v
ML Model Artifacts
```

### Vercel Configuration

The project uses `vercel.json` to route requests between the frontend and FastAPI backend.

Production API requests use:

```text
/api/*
```

while frontend resources are served from:

```text
/frontend/*
```

The frontend communicates with the backend using a relative API base URL:

```javascript
const API_BASE_URL = '/api';
```

This allows the same frontend code to work with the deployed Vercel application without hardcoding a local server address.

---

## Environment Variables

The production backend uses the following environment variables:

| Variable     | Description                                               |
| ------------ | --------------------------------------------------------- |
| `HF_REPO_ID` | Hugging Face repository containing model artifacts        |
| `HF_TOKEN`   | Hugging Face access token when authentication is required |

Example:

```text
HF_REPO_ID=lyca-byte/business-revenue-prediction-model
HF_TOKEN=<your-token>
```

These values should be configured through the Vercel project environment settings rather than hardcoded into source code.

---

## Model Loading in Production

The deployed backend does not depend on writing model files to the Vercel project filesystem.

Instead, the model loader retrieves the required artifacts from Hugging Face Hub:

```text
Hugging Face Hub
        |
        +-- revenue_prediction_model.pkl
        |
        +-- preprocessing.pkl
        |
        +-- model_metadata.json
```

The artifacts are cached in the temporary runtime directory:

```text
/tmp/huggingface
```

This approach is used because the Vercel serverless runtime does not provide a persistent writable application filesystem.

---

## Key Design Decisions

### Why Linear Regression?

Linear Regression provides a simple and interpretable baseline for predicting business revenue from numerical business variables.

It also allows the project to demonstrate:

* Feature preprocessing
* Model training
* Validation
* Test evaluation
* Coefficient interpretation
* Model serving through an API

### Why StandardScaler?

StandardScaler is fitted using the training data and reused during inference.

The same fitted scaler must be applied to incoming user data to ensure that the prediction input is represented in the same numerical space used during model training.

### Why Separate Validation and Test Data?

The validation set is used during model development and evaluation, while the test set is kept isolated for final performance assessment.

This reduces the risk of using test data to influence model development decisions.

### Why Hugging Face Hub?

The trained model artifacts are separated from the application deployment and stored in a dedicated Hugging Face repository.

This provides a practical way to manage Machine Learning model files without requiring the Vercel deployment to contain all model artifacts directly.

### Why FastAPI?

FastAPI provides:

* Lightweight REST API development
* Automatic request validation
* Pydantic integration
* Interactive API documentation
* Straightforward integration with Python Machine Learning models
* Compatibility with serverless deployment

### Why Vanilla JavaScript?

The frontend intentionally uses HTML, CSS, and Vanilla JavaScript rather than a frontend framework.

This keeps the application lightweight while demonstrating fundamental web development concepts such as:

* DOM manipulation
* Fetch API
* Event handling
* Form processing
* Client-side data visualization
* API integration

---

## Results and Visualizations

The project contains visualization outputs generated during exploratory analysis and model evaluation.

```text
results/visualizations/
|
├── distributions/
|   ├── feature_distributions.png
|   ├── feature_boxplots.png
|   └── revenue_distribution.png
|
├── correlation/
|   ├── correlation_heatmap.png
|   └── revenue_correlations.png
|
├── scatter_plots/
|   ├── features_vs_revenue.png
|   └── previous_revenue_vs_revenue.png
|
└── model_evaluation/
    ├── actual_vs_predicted.png
    ├── residual_analysis.png
    └── feature_coefficients.png
```

These visualizations support both exploratory data analysis and model evaluation.

---

## Development Status

| Phase | Description                              | Status   |
| ----- | ---------------------------------------- | -------- |
| 1     | Project Setup                            | Complete |
| 2     | Synthetic Dataset Generation             | Complete |
| 3     | Exploratory Data Analysis                | Complete |
| 4     | Data Preparation and Feature Engineering | Complete |
| 5     | Model Training                           | Complete |
| 6     | Model Evaluation and Saving              | Complete |
| 7     | FastAPI Backend                          | Complete |
| 8     | Frontend Development                     | Complete |
| 9     | Frontend and Backend Integration         | Complete |
| 10    | Hugging Face Model Hosting               | Complete |
| 11    | Vercel Deployment                        | Complete |
| 12    | Production Testing                       | Complete |
| 13    | Documentation                            | Complete |

---

## Future Improvements

Potential future improvements include:

* Experimenting with additional regression algorithms
* Hyperparameter optimization
* Comparing multiple Machine Learning models
* Adding confidence or prediction intervals
* Adding more business analytics features
* Adding authentication and user-specific prediction history
* Containerized deployment using Docker
* Automated model retraining pipelines
* Continuous integration and continuous deployment
* Monitoring model performance after deployment

---

## License

For educational and portfolio purposes.

IBM SkillsBuild University Education × Hacktiv8 Capstone Design Project.
