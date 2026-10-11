
from pathlib import Path

import joblib
import pandas as pd

# Locate the saved model
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_FILE = BASE_DIR / "backend" / "generation_model.joblib"

# Load the trained model
model = joblib.load(MODEL_FILE)


def predict_generation(
    irradiance_wm2,
    wind_speed_ms,
    temperature_c,
    outage_flag,
):
    # Arrange the input values in the same feature order used for training
    input_data = pd.DataFrame([{
        "irradiance_wm2": irradiance_wm2,
        "wind_speed_ms": wind_speed_ms,
        "temperature_c": temperature_c,
        "outage_flag": outage_flag,
    }])

    # Generate a prediction
    prediction = model.predict(input_data)[0]

    return round(float(prediction), 2)


# Test the prediction function
if __name__ == "__main__":
    result = predict_generation(
        irradiance_wm2=600,
        wind_speed_ms=7,
        temperature_c=32,
        outage_flag=0,
    )

    print("Predicted generation:", result, "MWh")
