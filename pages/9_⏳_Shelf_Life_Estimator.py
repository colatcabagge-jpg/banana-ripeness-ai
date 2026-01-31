import streamlit as st

st.set_page_config(
    page_title="Shelf Life Estimator | CVLab",
    layout="wide"
)

st.title("⏳ Banana Shelf-Life Estimation")
st.caption("Heuristic-based post-prediction decision support")

st.divider()

# --------------------------------------------------
# Explanation
# --------------------------------------------------
st.markdown(
    """
This module estimates **remaining usable shelf life** based on the predicted
ripeness stage and model confidence.

⚠️ **Important:**  
This is a **decision-support heuristic**, not a chemical or biological guarantee.
Actual shelf life depends on storage conditions such as temperature and humidity.
"""
)

st.divider()

# --------------------------------------------------
# Inputs (from inference)
# --------------------------------------------------
st.subheader("Prediction Inputs")

ripeness = st.selectbox(
    "Predicted Ripeness Stage",
    ["unripe", "ripe", "overripe", "rotten"]
)

confidence = st.slider(
    "Model Confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.75,
    step=0.01
)

# --------------------------------------------------
# Shelf-life logic
# --------------------------------------------------
BASE_DAYS = {
    "unripe": 5.0,
    "ripe": 2.0,
    "overripe": 0.7,
    "rotten": 0.0
}

estimated_days = round(BASE_DAYS[ripeness] * confidence, 2)

# --------------------------------------------------
# Output
# --------------------------------------------------
st.subheader("Estimated Shelf Life")

c1, c2 = st.columns(2)

c1.metric("Days Remaining", f"{estimated_days} days")
c2.metric("Confidence Used", f"{confidence*100:.1f}%")

# --------------------------------------------------
# Recommendations
# --------------------------------------------------
st.subheader("Usage Recommendation")

if ripeness == "unripe":
    st.success("Store at room temperature. Suitable for later consumption.")
elif ripeness == "ripe":
    st.info("Consume soon or refrigerate to slow ripening.")
elif ripeness == "overripe":
    st.warning("Use immediately for smoothies, baking, or cooking.")
else:
    st.error("Not recommended for consumption.")

# --------------------------------------------------
# Disclaimer
# --------------------------------------------------
st.divider()
st.caption(
    "Shelf-life estimation is heuristic-based and intended for educational and research use."
)
