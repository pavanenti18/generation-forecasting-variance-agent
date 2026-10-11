
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Locate the project and dataset
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "generation_forecast.csv"

# Load the dataset and sort it by date
df = pd.read_csv(DATA_FILE)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date", kind="stable").reset_index(drop=True)

# Select input features
features = [
    "irradiance_wm2",
    "wind_speed_ms",
    "temperature_c",
    "outage_flag",
]

X = df[features]
y = df["actual_mwh"]

# Use earlier observations for training and later ones for testing
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Train the regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
MODEL_FILE = BASE_DIR / "backend" / "generation_model.joblib"
joblib.dump(model, MODEL_FILE)

print("Saved model to:", MODEL_FILE)


# Predict generation for the test period
predictions = model.predict(X_test)


# Simple baseline: predict the training-set average for every test row
mean_prediction = y_train.mean()
mean_predictions = np.full(len(y_test), mean_prediction)

# Evaluate all three approaches on the same test rows
model_mae = mean_absolute_error(y_test, predictions)

mean_baseline_mae = mean_absolute_error(
    y_test,
    mean_predictions,
)

baseline_mae = mean_absolute_error(
    y_test,
    df["forecast_mwh"].iloc[split_index:]
)

rmse = np.sqrt(mean_squared_error(y_test, predictions))


print("FORECASTING MODEL EVALUATION")
print("----------------------------")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print(f"Regression model MAE: {model_mae:.2f} MWh")
print(f"Mean baseline MAE: {mean_baseline_mae:.2f} MWh")
print(f"Existing forecast MAE: {baseline_mae:.2f} MWh")
print(f"Regression model RMSE: {rmse:.2f} MWh")
print(f"Training-set mean prediction: {mean_prediction:.2f} MWh")



# Save summary metrics for the project evaluation report
metrics = pd.DataFrame([
    {
        "method": "Linear Regression",
        "MAE_MWh": model_mae,
        "RMSE_MWh": rmse,
    },
    {
        "method": "Mean Baseline",
        "MAE_MWh": mean_baseline_mae,
        "RMSE_MWh": np.sqrt(
            mean_squared_error(y_test, mean_predictions)
        ),
    },
    {
        "method": "Existing Forecast",
        "MAE_MWh": baseline_mae,
        "RMSE_MWh": np.sqrt(
            mean_squared_error(
                y_test,
                df["forecast_mwh"].iloc[split_index:]
            )
        ),
    },
])

METRICS_FILE = BASE_DIR / "data" / "evaluation_metrics.csv"
metrics.round(2).to_csv(METRICS_FILE, index=False)

print("Saved evaluation metrics to:", METRICS_FILE)



print("\nMODEL COMPARISON")
print("----------------")

if model_mae < baseline_mae and model_mae < mean_baseline_mae:
    print("Result: Regression model performed best on this test period.")
elif baseline_mae < model_mae and baseline_mae < mean_baseline_mae:
    print("Result: Existing forecast performed best on this test period.")
elif mean_baseline_mae < model_mae and mean_baseline_mae < baseline_mae:
    print("Result: Mean baseline performed best on this test period.")
else:
    print("Result: There is a tie or no single best method.")


# Display actual and predicted generation
results = pd.DataFrame({
    "date": df["date"].iloc[split_index:].dt.strftime("%Y-%m-%d"),
    "actual_mwh": y_test.to_numpy(),
    "regression_prediction_mwh": predictions,
    "existing_forecast_mwh": df["forecast_mwh"].iloc[
        split_index:
    ].to_numpy(),
})

print("\nTEST PERIOD PREDICTIONS")
print("-----------------------")
print(results.round(2).to_string(index=False))

# Save test-period predictions for evaluation
RESULTS_FILE = BASE_DIR / "data" / "evaluation_predictions.csv"
results.round(2).to_csv(RESULTS_FILE, index=False)

print("\nSaved evaluation predictions to:", RESULTS_FILE)