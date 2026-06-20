"""
Valid feature values and suggested ranges for sugarcane yield prediction.
Keep in sync with the training dataset (see generate_dataset.py).
"""

STATES = [
    "Maharashtra",
    "Uttar Pradesh",
    "Karnataka",
    "Tamil Nadu",
    "Bihar",
]

SOIL_TYPES = ["Alluvial", "Black", "Red", "Laterite"]

IRRIGATION_TYPES = ["Drip", "Flood", "Sprinkler"]

NUMERIC_FIELDS = {
    "area_acres": {
        "label": "Farm area",
        "min": 1.0,
        "max": 50.0,
        "default": 10.0,
        "step": 0.5,
        "unit": "acres",
        "help": "Total cultivated area under sugarcane (typical small farm: 5–25 acres).",
    },
    "rainfall_mm": {
        "label": "Annual rainfall",
        "min": 800.0,
        "max": 2500.0,
        "default": 1200.0,
        "step": 50.0,
        "unit": "mm",
        "help": "Average annual rainfall for the region (sugarcane prefers 900–1800 mm).",
    },
    "temp_c": {
        "label": "Average temperature",
        "min": 20.0,
        "max": 38.0,
        "default": 28.0,
        "step": 0.5,
        "unit": "°C",
        "help": "Mean growing-season temperature (ideal around 26–30 °C).",
    },
    "crop_age": {
        "label": "Crop age",
        "min": 10,
        "max": 18,
        "default": 12,
        "step": 1,
        "unit": "months",
        "help": "Months since planting (most varieties mature in 12–18 months).",
    },
    "fertilizer_kg": {
        "label": "Total fertilizer used",
        "min": 100.0,
        "max": 15000.0,
        "default": 1500.0,
        "step": 50.0,
        "unit": "kg",
        "help": "Total fertilizer applied to the field (often 100–300 kg per acre).",
    },
}

CATEGORICAL_FIELDS = {
    "state": {
        "label": "State",
        "options": STATES,
        "default": "Maharashtra",
        "help": "Indian state where the crop is grown.",
    },
    "soil_type": {
        "label": "Soil type",
        "options": SOIL_TYPES,
        "default": "Black",
        "help": "Dominant soil type in the field.",
    },
    "irrigation_type": {
        "label": "Irrigation type",
        "options": IRRIGATION_TYPES,
        "default": "Drip",
        "help": "Primary irrigation method used.",
    },
}
