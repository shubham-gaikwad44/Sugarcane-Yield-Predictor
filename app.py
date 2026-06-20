import streamlit as st

from src.feature_options import CATEGORICAL_FIELDS, NUMERIC_FIELDS
from src.yield_prediction import predict_yield, validate_inputs

st.set_page_config(
    page_title="Sugarcane Yield Advisor",
    page_icon="🌾",
    layout="centered",
)

st.title("🌾 Sugarcane Yield Predictor")
st.caption("Enter your farm details to estimate yield (tons per acre).")

with st.form("yield_form"):
    st.subheader("Location & field")
    col1, col2 = st.columns(2)

    with col1:
        state = st.selectbox(
            CATEGORICAL_FIELDS["state"]["label"],
            CATEGORICAL_FIELDS["state"]["options"],
            index=CATEGORICAL_FIELDS["state"]["options"].index(
                CATEGORICAL_FIELDS["state"]["default"]
            ),
            help=CATEGORICAL_FIELDS["state"]["help"],
        )
        soil_type = st.selectbox(
            CATEGORICAL_FIELDS["soil_type"]["label"],
            CATEGORICAL_FIELDS["soil_type"]["options"],
            index=CATEGORICAL_FIELDS["soil_type"]["options"].index(
                CATEGORICAL_FIELDS["soil_type"]["default"]
            ),
            help=CATEGORICAL_FIELDS["soil_type"]["help"],
        )

    with col2:
        area_cfg = NUMERIC_FIELDS["area_acres"]
        area_acres = st.number_input(
            f"{area_cfg['label']} ({area_cfg['unit']})",
            min_value=float(area_cfg["min"]),
            max_value=float(area_cfg["max"]),
            value=float(area_cfg["default"]),
            step=float(area_cfg["step"]),
            help=area_cfg["help"],
        )
        irrigation_type = st.selectbox(
            CATEGORICAL_FIELDS["irrigation_type"]["label"],
            CATEGORICAL_FIELDS["irrigation_type"]["options"],
            index=CATEGORICAL_FIELDS["irrigation_type"]["options"].index(
                CATEGORICAL_FIELDS["irrigation_type"]["default"]
            ),
            help=CATEGORICAL_FIELDS["irrigation_type"]["help"],
        )

    st.subheader("Climate & crop")
    col3, col4 = st.columns(2)

    with col3:
        rain_cfg = NUMERIC_FIELDS["rainfall_mm"]
        rainfall_mm = st.slider(
            f"{rain_cfg['label']} ({rain_cfg['unit']})",
            min_value=float(rain_cfg["min"]),
            max_value=float(rain_cfg["max"]),
            value=float(rain_cfg["default"]),
            step=float(rain_cfg["step"]),
            help=rain_cfg["help"],
        )
        age_cfg = NUMERIC_FIELDS["crop_age"]
        crop_age = st.select_slider(
            f"{age_cfg['label']} ({age_cfg['unit']})",
            options=list(range(int(age_cfg["min"]), int(age_cfg["max"]) + 1)),
            value=int(age_cfg["default"]),
            help=age_cfg["help"],
        )

    with col4:
        temp_cfg = NUMERIC_FIELDS["temp_c"]
        temp_c = st.slider(
            f"{temp_cfg['label']} ({temp_cfg['unit']})",
            min_value=float(temp_cfg["min"]),
            max_value=float(temp_cfg["max"]),
            value=float(temp_cfg["default"]),
            step=float(temp_cfg["step"]),
            help=temp_cfg["help"],
        )
        fert_cfg = NUMERIC_FIELDS["fertilizer_kg"]
        fertilizer_kg = st.number_input(
            f"{fert_cfg['label']} ({fert_cfg['unit']})",
            min_value=float(fert_cfg["min"]),
            max_value=float(fert_cfg["max"]),
            value=float(fert_cfg["default"]),
            step=float(fert_cfg["step"]),
            help=fert_cfg["help"],
        )

    submitted = st.form_submit_button("Predict yield", type="primary", use_container_width=True)

if submitted:
    try:
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
        predicted = predict_yield(
            state=state,
            area_acres=area_acres,
            rainfall_mm=rainfall_mm,
            temp_c=temp_c,
            soil_type=soil_type,
            irrigation_type=irrigation_type,
            crop_age=crop_age,
            fertilizer_kg=fertilizer_kg,
        )
        total_yield = round(predicted * area_acres, 2)

        st.success(f"**Estimated yield: {predicted} tons/acre**")
        st.info(f"Total expected harvest for {area_acres} acres: **{total_yield} tons**")
    except (ValueError, FileNotFoundError) as exc:
        st.error(str(exc))

with st.expander("Suggested reference values"):
    st.markdown(
        """
        | Field | Suggested options / range |
        |---|---|
        | **State** | Maharashtra, Uttar Pradesh, Karnataka, Tamil Nadu, Bihar |
        | **Area** | 1–50 acres (typical: 5–25) |
        | **Rainfall** | 800–2500 mm (ideal: 900–1800) |
        | **Temperature** | 20–38 °C (ideal: 26–30) |
        | **Soil** | Alluvial, Black, Red, Laterite |
        | **Irrigation** | Drip (best), Sprinkler, Flood |
        | **Crop age** | 10–18 months (common: 12–15) |
        | **Fertilizer** | ~100–300 kg per acre |
        """
    )
