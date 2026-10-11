# Power Generation Forecasting & Variance Explanation Agent

A Python-based prototype for renewable energy generation prediction, forecast variance analysis, and rule-based explanations of possible forecast-miss drivers.

## 1. Project Overview

This application combines a machine-learning baseline with a lightweight explanation component. Users can enter weather conditions, an outage flag, and a supplied forecast through a web interface. The backend returns a generation prediction and compares it with the supplied forecast.

When actual generation is provided, the application also calculates the forecast error and reports possible contributing factors.

## 2. Features

- Generation prediction using a Linear Regression model.
- Forecast comparison and variance calculation.
- Rule-based explanations using irradiance, wind speed, temperature, and outage status.
- FastAPI backend with input validation.
- HTML, CSS, and JavaScript frontend.
- Automated API and explanation tests.
- Evaluation against a mean baseline and the supplied forecast.

## 3. Technology Stack

- Python 3.11
- FastAPI and Uvicorn
- Pandas and NumPy
- Scikit-learn and Joblib
- HTML, CSS, and JavaScript
- Pytest and HTTPX

## 4. Project Structure

```text
backend/
  app.py
  explanation.py
  train_model.py
  predict.py
data/
  generation_forecast.csv
  evaluation_predictions.csv
  evaluation_metrics.csv
frontend/
  index.html
tests/
  test_api.py
  test_explanation.py
requirements.txt
Procfile
README.md
```

## 5. Dataset

The bundled dataset contains 60 observations and the following columns:

- `date`: observation date
- `irradiance_wm2`: solar irradiance in W/m²
- `wind_speed_ms`: wind speed in m/s
- `temperature_c`: temperature in °C
- `outage_flag`: outage indicator
- `forecast_mwh`: supplied generation forecast in MWh
- `actual_mwh`: observed generation in MWh

The dataset is synthetic/dummy assessment data and should not be interpreted as verified operational data from a real power plant.

## 6. Setup and Run Locally

### Prerequisites

Install Python 3.11 or a compatible version and Git.

### Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Start the backend

From the project root:

```powershell
uvicorn backend.app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### Open the frontend

Open `frontend/index.html` in a browser while the backend is running.

## 7. API Endpoints

- `GET /api/demo`: basic service status.
- `POST /api/run`: generate a prediction and compare it with the supplied forecast.

Example request body:

```json
{
  "irradiance_wm2": 572.9,
  "wind_speed_ms": 4.59,
  "temperature_c": 35.4,
  "outage_flag": 1,
  "forecast_mwh": 21.36,
  "actual_mwh": 4.19
}
```

The response includes the predicted generation, supplied forecast, prediction-versus-forecast variance, and—when actual generation is supplied—forecast error and possible drivers.

**Variance conventions:**
- Prediction versus supplied forecast = predicted generation − supplied forecast.
- Forecast error = actual generation − supplied forecast.
- Positive forecast error indicates underforecasting.
- Negative forecast error indicates overforecasting.

## 8. Model and Evaluation

The forecasting model is a Scikit-learn Linear Regression model using irradiance, wind speed, temperature, and outage status as input features.

The data is sorted chronologically and split into training and test portions. The supplied forecast and a mean baseline are evaluated on the same test rows.

Recorded test-set results:

| Method | MAE (MWh) | RMSE (MWh) |
|---|---:|---:|
| Linear Regression | 6.32 | 7.75 |
| Mean Baseline | 11.86 | 14.96 |
| Supplied Forecast | 4.60 | 5.17 |

On this test split, the supplied forecast performs better than the trained Linear Regression model. This is an important finding: the new model does not outperform the existing forecast on the available test data.

Detailed results are stored in `data/evaluation_metrics.csv` and `data/evaluation_predictions.csv`.

## 9. Run the Evaluation and Tests

Retrain the model and regenerate evaluation outputs:

```powershell
python -m backend.train_model
```

Run the automated tests:

```powershell
python -m pytest tests -v
```

The current automated test suite contains eight tests covering the API, input validation, and explanation behavior.

## 10. Explanation Logic

The explanation component uses predefined rules to flag possible drivers, including outages, low irradiance, high temperature, and low wind speed.

These are diagnostic hints, not proven causal explanations. An outage flag or high temperature may warrant investigation, but the current implementation cannot establish that either factor caused a forecast miss.

## 11. Assumptions and Limitations

- The dataset is small, with only 60 observations.
- The dataset has two observations per date but no explicit intraday timestamp or asset identifier.
- The outage flag is rare, limiting the evidence available to assess outage effects.
- The test set contains only 12 observations.
- Results may change substantially with different data and operating conditions.
- The Linear Regression model is a baseline, not a production forecasting system.
- The explanation component is rule-based; it does not use an LLM, RAG pipeline, or autonomous agent.
- The model does not account for all possible operational, seasonal, or asset-specific factors.
- The application has not been validated against real power-generation data.

## 12. Production Readiness and Future Work

Potential improvements include:

- Collecting larger, time-stamped operational datasets.
- Evaluating multiple forecasting models with time-aware validation.
- Adding asset identifiers and additional operational features.
- Improving outage and weather-related diagnostic analysis.
- Adding an LLM-based explanation layer with grounded evidence and safeguards.
- Adding monitoring, logging, authentication, and deployment-specific CORS settings.
- Deploying the application to Railway and verifying the public endpoints.

## 13. Deployment Status

Railway deployment and public URL verification are pending. Add the final deployment URL and screenshots here after deployment and testing.
