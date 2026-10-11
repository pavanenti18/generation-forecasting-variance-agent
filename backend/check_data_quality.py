
from pathlib import Path
import pandas as pd

# Locate and load the dataset
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "generation_forecast.csv"

df = pd.read_csv(DATA_FILE)
df["date"] = pd.to_datetime(df["date"])

print("DATA QUALITY CHECK")
print("------------------")
print("Total rows:", len(df))
print("Missing values per column:")
print(df.isnull().sum().to_string())

# Count how many records exist for each date
print("\nRECORDS PER DATE")
print("----------------")
print(df["date"].value_counts().sort_index().to_string())

# Display rows for dates that occur more than once
duplicate_dates = df[df.duplicated(subset=["date"], keep=False)]
print("\nROWS WITH DUPLICATE DATES")
print("-------------------------")

if duplicate_dates.empty:
    print("No duplicate dates found.")
else:
    print(
        duplicate_dates.sort_values("date")
        .to_string(index=False)
    )

# Check whether the dataset is already in chronological order
print("\nCHRONOLOGICAL ORDER")
print("-------------------")
print("Already sorted:", df["date"].is_monotonic_increasing)
