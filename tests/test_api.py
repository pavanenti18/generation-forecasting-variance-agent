
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_demo_endpoint():
    response = client.get("/api/demo")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_run_endpoint_with_actual_generation():
    response = client.post(
        "/api/run",
        json={
            "irradiance_wm2": 572.9,
            "wind_speed_ms": 4.59,
            "temperature_c": 35.4,
            "outage_flag": 1,
            "forecast_mwh": 21.36,
            "actual_mwh": 4.19,
        },
    )

    assert response.status_code == 200

    result = response.json()
    assert result["predicted_generation_mwh"] == 12.73
    assert result["explanation"]["error_mwh"] == -17.17
    assert result["explanation"]["forecast_direction"] == "overforecast"


def test_run_endpoint_without_actual_generation():
    response = client.post(
        "/api/run",
        json={
            "irradiance_wm2": 600,
            "wind_speed_ms": 7,
            "temperature_c": 32,
            "outage_flag": 0,
            "forecast_mwh": 21.36,
        },
    )

    assert response.status_code == 200

    result = response.json()
    assert "explanation" not in result
    assert "actual_generation_mwh" not in result


def test_invalid_outage_flag_is_rejected():
    response = client.post(
        "/api/run",
        json={
            "irradiance_wm2": 600,
            "wind_speed_ms": 7,
            "temperature_c": 32,
            "outage_flag": 2,
            "forecast_mwh": 21.36,
        },
    )

    assert response.status_code == 422
