from pathlib import Path
import pandas as pd

# Locate and load the dataset
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "generation_forecast.csv"

df = pd.read_csv(DATA_FILE)

# Calculate the forecast error
df["error_mwh"] = df["actual_mwh"] - df["forecast_mwh"]
df["absolute_error_mwh"] = df["error_mwh"].abs()

# Select the five largest forecast misses
largest_misses = df.sort_values(
    by="absolute_error_mwh",
    ascending=False
).head(5)

# Display weather and outage information for those dates
columns_to_show = [
    "date",
    "irradiance_wm2",
    "wind_speed_ms",
    "temperature_c",
    "outage_flag",
    "forecast_mwh",
    "actual_mwh",
    "error_mwh",
    "absolute_error_mwh",
]

print("LARGEST FORECAST MISSES AND THEIR CONDITIONS")
print("--------------------------------------------")
print(largest_misses[columns_to_show].round(2).to_string(index=False))

# Compare the outage flag across all observations
print("\nOUTAGE FLAG COUNTS")
print("------------------")
print(df["outage_flag"].value_counts().sort_index().to_string())