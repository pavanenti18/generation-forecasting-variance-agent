from pathlib import Path
import pandas as pd

# Step 1: Locate the project folder
PROJECT_FOLDER = Path(__file__).resolve().parents[1]

# Step 2: Locate the CSV dataset
DATASET_FILE = PROJECT_FOLDER / "data" / "generation_forecast.csv"

# Step 3: Load the dataset into a DataFrame
df = pd.read_csv(DATASET_FILE)

# Step 4: Display the first five rows
print("FIRST Ten ROWS")
print("----------------")
print(df.head(10))

# Step 5: Calculate average forecast generation
average_forecast = df["forecast_mwh"].mean()

print("\nAVERAGE FORECAST GENERATION")
print("-------------------------")
print(f"{average_forecast:.2f} MWh")

# Step 6:  Calculate average actual generation

average_actual = df["actual_mwh"].mean()

print("\nAVERAGE ACTUAL GENERATION")
print("-------------------------")
print(f"{average_actual:.2f} MWh")


# Step 7: Find the lowest actual generation
lowest_generation = df["actual_mwh"].min()

print("\nLOWEST ACTUAL GENERATION")
print("-------------------------")
print(f"{lowest_generation:.2f} MWh")

# Step 8: Find the highest actual generation
highest_generation = df["actual_mwh"].max()

print("\nHIGHEST ACTUAL GENERATION")
print("-------------------------")
print(f"{highest_generation:.2f} MWh")