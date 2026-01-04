import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Student Support Prediction")

st.title("Student Support Priority Prediction")

# Load model
model = pickle.load(open("student_model.pkl", "rb"))

st.write("Enter student details")

income = st.number_input("Family Annual Income", min_value=0)
orphan = st.selectbox("Is the student an Orphan?", [0, 1])
dropout = st.selectbox("Is the student a Dropout?", [0, 1])
bpl = st.selectbox("Below Poverty Line (BPL)?", [0, 1])

if st.button("Predict"):
    data = pd.DataFrame(
        [[income, orphan, dropout, bpl]],
        columns=["family_annual_income", "Orphan", "Dropout", "BPL"]
    )
    result = model.predict(data)
    st.success(f"Predicted Category: {result[0]}")
