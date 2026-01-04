# app.py
import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Student Support Prediction", layout="centered")

st.title("🎓 Student Support Prediction")

# ----------------------
# Load the trained model
# ----------------------
try:
    with open("student_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ Model file 'student_model.pkl' not found! Make sure it is in the same folder as app.py.")
    st.stop()

# ----------------------
# Input form for new student
# ----------------------
st.header("Enter Student Details:")

with st.form("student_form"):
    student_id = st.text_input("Student ID")
    orphan = st.selectbox("Orphan?", ["No", "Yes"])
    dropout = st.selectbox("Dropout?", ["No", "Yes"])
    bpl = st.selectbox("Below Poverty Line?", ["No", "Yes"])
    education_level = st.selectbox("Education Level", ["Below 12th", "Completed 12th", "Graduated"])
    family_status = st.selectbox("Family Status", ["Both Parents", "Single Parent", "No Parents"])
    annual_income = st.number_input("Family Annual Income", min_value=0)
    risk_severity_score = st.number_input("Risk Severity Score", min_value=0)

    submitted = st.form_submit_button("Predict Support Priority")

# ----------------------
# Process input and predict
# ----------------------
if submitted:
    # Convert inputs to DataFrame
    input_data = pd.DataFrame({
        "orphan": [1 if orphan=="Yes" else 0],
        "dropout": [1 if dropout=="Yes" else 0],
        "below_poverty_line": [1 if bpl=="Yes" else 0],
        "education_level": [education_level],
        "family_status": [family_status],
        "family_annual_income": [annual_income],
        "risk_severity_score": [risk_severity_score]
    })

    try:
        prediction = model.predict(input_data)[0]
        if prediction == 1:
            result = "✅ Help Needed"
        elif prediction == 2:
            result = "⚠️ Intermediate Support Needed"
        elif prediction == 3:
            result = "🔥 Urgent Support Needed"
        else:
            result = "Unknown"

        st.success(f"Prediction for Student {student_id}: {result}")

    except Exception as e:
        st.error(f"Error during prediction: {e}")
