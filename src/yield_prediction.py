import os
import joblib
import pandas as pd

from src.feature_options import (
    CATEGORICAL_FIELDS,
    IRRIGATION_TYPES,
    NUMERIC_FIELDS,
    SOIL_TYPES,
    STATES,
)


def validate_inputs(
    state,
    area_acres,
    rainfall_mm,
    temp_c,
    soil_type,
    irrigation_type,
    crop_age,
    fertilizer_kg,
):
    """Validate user input against known training-data options and ranges."""
    if state not in STATES:
        raise ValueError(f"State must be one of: {', '.join(STATES)}")
    if soil_type not in SOIL_TYPES:
        raise ValueError(f"Soil type must be one of: {', '.join(SOIL_TYPES)}")
    if irrigation_type not in IRRIGATION_TYPES:
        raise ValueError(
            f"Irrigation type must be one of: {', '.join(IRRIGATION_TYPES)}"
        )

    checks = [
        ("area_acres", area_acres),
        ("rainfall_mm", rainfall_mm),
        ("temp_c", temp_c),
        ("crop_age", crop_age),
        ("fertilizer_kg", fertilizer_kg),
    ]
    for field_name, value in checks:
        cfg = NUMERIC_FIELDS[field_name]
        if not (cfg["min"] <= value <= cfg["max"]):
            raise ValueError(
                f"{cfg['label']} must be between {cfg['min']} and {cfg['max']} {cfg['unit']}"
            )


def predict_yield(state, area_acres, rainfall_mm, temp_c, soil_type, irrigation_type, crop_age, fertilizer_kg):
    """
    Predicts the sugarcane yield (tons per acre) using the trained ML model.
    """
    validate_inputs(
        state=state,
        area_acres=area_acres,
        rainfall_mm=rainfall_mm,
        temp_c=temp_c,
        soil_type=soil_type,
        irrigation_type=irrigation_type,
        crop_age=crop_age,
        fertilizer_kg=fertilizer_kg,
    )

    model_path = "models/yield_model.pkl"

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Trained model not found at {model_path}. Please train the model first."
        )

    pipeline = joblib.load(model_path)

    input_data = pd.DataFrame(
        [
            {
                "State": state,
                "Area_Acres": area_acres,
                "Rainfall_mm": rainfall_mm,
                "Temperature_C": temp_c,
                "Soil_Type": soil_type,
                "Irrigation_Type": irrigation_type,
                "Crop_Age_Months": crop_age,
                "Fertilizer_Used_kg": fertilizer_kg,
            }
        ]
    )

    prediction = pipeline.predict(input_data)
    return round(prediction[0], 2)


def _prompt_choice(label, options, default):
    print(f"\n{label}")
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")
    while True:
        raw = input(f"Choose (1-{len(options)}) [{default}]: ").strip()
        if not raw:
            return default
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("Invalid choice. Enter a number from the list.")


def _prompt_number(field_name):
    cfg = NUMERIC_FIELDS[field_name]
    print(f"\n{cfg['label']} ({cfg['unit']})")
    print(f"  Suggested range: {cfg['min']}–{cfg['max']}")
    print(f"  {cfg['help']}")
    while True:
        raw = input(f"Enter value [{cfg['default']}]: ").strip()
        if not raw:
            return cfg["default"] if field_name != "crop_age" else int(cfg["default"])
        try:
            value = float(raw) if field_name != "crop_age" else int(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if cfg["min"] <= value <= cfg["max"]:
            return value
        print(f"Value must be between {cfg['min']} and {cfg['max']}.")


def collect_user_input():
    """Interactive CLI to collect farm details with suggested options."""
    print("=== Sugarcane Yield Predictor ===")
    print("Select from the suggested options below.\n")

    state = _prompt_choice(
        CATEGORICAL_FIELDS["state"]["label"],
        CATEGORICAL_FIELDS["state"]["options"],
        CATEGORICAL_FIELDS["state"]["default"],
    )
    soil_type = _prompt_choice(
        CATEGORICAL_FIELDS["soil_type"]["label"],
        CATEGORICAL_FIELDS["soil_type"]["options"],
        CATEGORICAL_FIELDS["soil_type"]["default"],
    )
    irrigation_type = _prompt_choice(
        CATEGORICAL_FIELDS["irrigation_type"]["label"],
        CATEGORICAL_FIELDS["irrigation_type"]["options"],
        CATEGORICAL_FIELDS["irrigation_type"]["default"],
    )

    area_acres = _prompt_number("area_acres")
    rainfall_mm = _prompt_number("rainfall_mm")
    temp_c = _prompt_number("temp_c")
    crop_age = _prompt_number("crop_age")
    fertilizer_kg = _prompt_number("fertilizer_kg")

    return {
        "state": state,
        "area_acres": area_acres,
        "rainfall_mm": rainfall_mm,
        "temp_c": temp_c,
        "soil_type": soil_type,
        "irrigation_type": irrigation_type,
        "crop_age": crop_age,
        "fertilizer_kg": fertilizer_kg,
    }


if __name__ == "__main__":
    inputs = collect_user_input()
    predicted_yield = predict_yield(**inputs)
    total_yield = round(predicted_yield * inputs["area_acres"], 2)

    print("\n--- Result ---")
    print(f"Predicted yield: {predicted_yield} tons/acre")
    print(f"Total for {inputs['area_acres']} acres: {total_yield} tons")
