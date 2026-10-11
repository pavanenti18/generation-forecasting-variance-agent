def explain_forecast_miss(
    forecast_mwh,
    actual_mwh,
    irradiance_wm2,
    wind_speed_ms,
    temperature_c,
    outage_flag,
):
    # Calculate the forecast error.
    error_mwh = actual_mwh - forecast_mwh
    absolute_error = abs(error_mwh)

    # Classify the forecast direction.
    if error_mwh > 0:
        direction = "underforecast"
    elif error_mwh < 0:
        direction = "overforecast"
    else:
        direction = "exact forecast"

    # Start with the observed conditions.
    reasons = []

    if outage_flag == 1:
        reasons.append(
            "An outage was flagged and may have reduced generation."
        )

    # Report weather observations without assuming causation.
    if irradiance_wm2 < 500:
        reasons.append(
            "Irradiance was below 500 W/m²; this may be relevant "
            "for solar generation."
        )

    if temperature_c >= 35:
        reasons.append(
            "Temperature was at least 35°C; investigate whether "
            "heat affected asset performance."
        )

    if wind_speed_ms < 4:
        reasons.append(
            "Wind speed was below 4 m/s; this may matter for "
            "wind generation."
        )

    if not reasons:
        reasons.append(
            "No predefined warning condition was triggered. "
            "Further operational analysis may be needed."
        )

    return {
        "forecast_mwh": forecast_mwh,
        "actual_mwh": actual_mwh,
        "error_mwh": round(error_mwh, 2),
        "absolute_error_mwh": round(absolute_error, 2),
        "forecast_direction": direction,
        "irradiance_wm2": irradiance_wm2,
        "wind_speed_ms": wind_speed_ms,
        "temperature_c": temperature_c,
        "outage_flag": outage_flag,
        "possible_drivers": reasons,
    }



if __name__ == "__main__":
    # Test using the August 15 observation.
    result = explain_forecast_miss(
        forecast_mwh=21.36,
        actual_mwh=4.19,
        irradiance_wm2=572.9,
        wind_speed_ms=4.59,
        temperature_c=35.4,
        outage_flag=1,
    )

    print("FORECAST EXPLANATION")
    print("--------------------")

    for key, value in result.items():
        print(f"{key}: {value}")
