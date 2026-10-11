from pathlib import Path
import pandas as pd

# Step 1: Locate the project and dataset
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "generation_forecast.csv"

# Step 2: Load the dataset
df = pd.read_csv(DATA_FILE)

# Step 3: Display dataset overview
print("DATASET OVERVIEW")
print("----------------")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))
print("Columns:", list(df.columns))

# Step 4: Calculate forecast error
# Positive error = underforecast
# Negative error = overforecast
df["error_mwh"] = df["actual_mwh"] - df["forecast_mwh"]

# Step 5: Calculate absolute forecast error
df["absolute_error_mwh"] = df["error_mwh"].abs()

# Step 6: Display the first 10 forecast errors
print("\nFIRST 10 FORECAST ERRORS")
print("------------------------")

print(
    df[
        [
            "date",
            "forecast_mwh",
            "actual_mwh",
            "error_mwh",
            "absolute_error_mwh",
        ]
    ].head(10).round(2).to_string(index=False)
)

# Step 7: Calculate baseline forecast metrics
print("\nBASELINE FORECAST METRICS")
print("-------------------------")

mae = df["absolute_error_mwh"].mean()
mean_signed_error = df["error_mwh"].mean()

print("Mean absolute error (MWh):", round(mae, 2))
print("Mean signed error (MWh):", round(mean_signed_error, 2))

# Step 8: Classify forecast errors
def classify_forecast(error):
    if error > 0:
        return "Underforecast"
    elif error < 0:
        return "Overforecast"
    else:
        return "Exact forecast"


df["forecast_status"] = df["error_mwh"].apply(classify_forecast)

print("\nFORECAST STATUS COUNTS")
print("----------------------")
print(df["forecast_status"].value_counts().to_string())

# Step 9: Find the five largest forecast errors
largest_errors = df.sort_values(
    by="absolute_error_mwh",
    ascending=False
).head(5)

print("\nFIVE LARGEST FORECAST ERRORS")
print("----------------------------")

print(
    largest_errors[
        [
            "date",
            "forecast_mwh",
            "actual_mwh",
            "error_mwh",
            "absolute_error_mwh",
            "forecast_status",
        ]
    ].round(2).to_string(index=False)
)