import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open("student_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🎓 Student Support Priority Prediction")
st.write("Enter student details to predict support priority")

# ---- USER INPUTS ----
orphan = st.selectbox("Is the student an Orphan?", ["No", "Yes"])
dropout = st.selectbox("Is the student a Dropout?", ["No", "Yes"])
bpl = st.selectbox("Below Poverty Line (BPL)?", ["No", "Yes"])

income = st.number_input("Family Annual Income", min_value=0)
risk_score = st.slider("Risk Severity Score", 0, 10, 5)

# Convert inputs
data = {
    "Orphan": 1 if orphan == "Yes" else 0,
    "Dropout": 1 if dropout == "Yes" else 0,
    "Below_Poverty_Line": 1 if bpl == "Yes" else 0,
    "family_annual_income": income,
    "risk_severity_score": risk_score
}

input_df = pd.DataFrame([data])

# ---- PREDICTION ----
if st.button("Predict Support Level"):
    prediction = model.predict(input_df)[0]

    if prediction == 3:
        st.error("🚨 URGENT HELP NEEDED")
    elif prediction == 2:
        st.warning("⚠️ INTERMEDIATE HELP NEEDED")
    else:
        st.success("✅ HELP NEEDED (LOW PRIORITY)")
