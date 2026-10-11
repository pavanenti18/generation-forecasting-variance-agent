from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.predict import predict_generation
from backend.explanation import explain_forecast_miss

app = FastAPI(
    title="Power Generation Forecasting & Variance Explanation Agent"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"


class Query(BaseModel):
    text: str = ""


class ForecastRequest(BaseModel):
    irradiance_wm2: float = Field(ge=0)
    wind_speed_ms: float = Field(ge=0)
    temperature_c: float
    outage_flag: int = Field(ge=0, le=1)
    forecast_mwh: float = Field(ge=0)
    actual_mwh: float | None = Field(default=None, ge=0)


@app.get("/api/demo")
def demo():
    return {
        "case_study": "Power Generation Forecasting & Variance Explanation Agent",
        "status": "running",
        "features": [
            "Generation prediction",
            "Forecast variance analysis",
            "Rule-based explanation of possible drivers",
        ],
    }


@app.post("/api/run")
def run_case(request: ForecastRequest):
    try:
        predicted_mwh = predict_generation(
            irradiance_wm2=request.irradiance_wm2,
            wind_speed_ms=request.wind_speed_ms,
            temperature_c=request.temperature_c,
            outage_flag=request.outage_flag,
        )

        result = {
            "predicted_generation_mwh": predicted_mwh,
            "supplied_forecast_mwh": request.forecast_mwh,
            "prediction_vs_forecast_variance_mwh": round(
                predicted_mwh - request.forecast_mwh, 2
            ),
        }

        if request.actual_mwh is not None:
            explanation = explain_forecast_miss(
                forecast_mwh=request.forecast_mwh,
                actual_mwh=request.actual_mwh,
                irradiance_wm2=request.irradiance_wm2,
                wind_speed_ms=request.wind_speed_ms,
                temperature_c=request.temperature_c,
                outage_flag=request.outage_flag,
            )

            result["actual_generation_mwh"] = request.actual_mwh
            result["explanation"] = explanation

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check the backend logs.",
        ) from exc
