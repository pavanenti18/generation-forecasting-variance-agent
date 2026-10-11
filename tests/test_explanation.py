
from backend.explanation import explain_forecast_miss


def test_overforecast():
    result = explain_forecast_miss(
        forecast_mwh=21.36,
        actual_mwh=4.19,
        irradiance_wm2=572.9,
        wind_speed_ms=4.59,
        temperature_c=35.4,
        outage_flag=1,
    )

    assert result["error_mwh"] == -17.17
    assert result["forecast_direction"] == "overforecast"


def test_underforecast():
    result = explain_forecast_miss(
        forecast_mwh=40,
        actual_mwh=50,
        irradiance_wm2=600,
        wind_speed_ms=7,
        temperature_c=30,
        outage_flag=0,
    )

    assert result["error_mwh"] == 10
    assert result["forecast_direction"] == "underforecast"


def test_exact_forecast():
    result = explain_forecast_miss(
        forecast_mwh=50,
        actual_mwh=50,
        irradiance_wm2=600,
        wind_speed_ms=7,
        temperature_c=30,
        outage_flag=0,
    )

    assert result["error_mwh"] == 0
    assert result["forecast_direction"] == "exact forecast"


def test_outage_is_reported_as_possible_driver():
    result = explain_forecast_miss(
        forecast_mwh=40,
        actual_mwh=30,
        irradiance_wm2=600,
        wind_speed_ms=7,
        temperature_c=30,
        outage_flag=1,
    )

    assert any(
        "outage was flagged" in reason
        for reason in result["possible_drivers"]
    )

