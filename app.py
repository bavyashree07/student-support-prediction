import streamlit as st
import pickle
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="Student Support Prediction")
st.title("Student Support Priority Prediction")

# Debug: check current folder contents
st.write("Files in current folder:", os.listdir())

# Load model safely
try:
    with open("student_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Model file 'student_model.pkl' not found! Make sure it is uploaded in the same folder as app.py.")
    st.stop()  # Stop running the app further

# User input
st.write("Enter student details")
income = st.number_input("Family Annual Income", min_value=0)
orphan = st.selectbox("Is the student an Orphan?", [0, 1])
dropout = st.selectbox("Is the student a Dropout?", [0, 1])
bpl = st.selectbox("Below Poverty Line (BPL)?", [0, 1])

# Prediction
if st.button("Predict"):
    data = pd.DataFrame(
        [[income, orphan, dropout, bpl]],
        columns=["family_annual_income", "Orphan", "Dropout", "BPL"]
    )
    result = model.predict(data)
    st.success(f"Predicted Category: {result[0]}")
