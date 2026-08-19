import streamlit as st
import pandas as pd
import joblib

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# Load Trained Model
# -------------------------------

model = joblib.load("student_model.pkl")

# -------------------------------
# Title
# -------------------------------

st.title("🎓 AI Student Performance Predictor")

st.write(
    "An AI-powered system that predicts student academic performance "
    "using Machine Learning."
)

st.divider()

# -------------------------------
# Student Information
# -------------------------------

st.subheader("👤 Student Information")

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

with col2:
    university_id = st.text_input(
        "University ID",
        placeholder="Enter university ID"
    )

st.divider()

# -------------------------------
# Academic Information
# -------------------------------

st.subheader("📊 Academic Information")

col1, col2, col3 = st.columns(3)

with col1:
    attendance = st.slider(
        "Attendance (%)",
        min_value=50,
        max_value=100,
        value=75
    )

    study_hours = st.slider(
        "Study Hours per Day",
        min_value=1,
        max_value=8,
        value=4
    )

with col2:
    assignment_score = st.slider(
        "Assignment Score",
        min_value=40,
        max_value=100,
        value=70
    )

    internal_marks = st.slider(
        "Internal Marks",
        min_value=35,
        max_value=100,
        value=70
    )

with col3:
    previous_gpa = st.slider(
        "Previous GPA",
        min_value=4.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )

    participation = st.slider(
        "Class Participation",
        min_value=1,
        max_value=10,
        value=6
    )

st.divider()

# -------------------------------
# Prediction
# -------------------------------

if st.button("🔮 Predict Student Performance"):

    # Check student details
    if student_name == "" or university_id == "":
        st.warning(
            "⚠️ Please enter both Student Name and University ID."
        )

    else:

        # Create input dataframe
        input_data = pd.DataFrame({
            "Attendance": [attendance],
            "Study_Hours": [study_hours],
            "Assignment_Score": [assignment_score],
            "Internal_Marks": [internal_marks],
            "Previous_GPA": [previous_gpa],
            "Participation": [participation]
        })

        # Prediction
        prediction = model.predict(input_data)[0]

        # Probability
        probability = model.predict_proba(input_data)[0][1]

        # -------------------------------
        # Student Details
        # -------------------------------

        st.divider()

        st.subheader("👨‍🎓 Student Details")

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:
            st.write(f"**Name:** {student_name}")

        with detail_col2:
            st.write(f"**University ID:** {university_id}")

        # -------------------------------
        # Prediction Result
        # -------------------------------

        st.subheader("🎯 Prediction Result")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:

            if prediction == 1:
                st.success("✅ PASS")
            else:
                st.error("❌ FAIL")

        with result_col2:

            st.metric(
                "Pass Probability",
                f"{probability * 100:.2f}%"
            )

        with result_col3:

            if probability >= 0.75:
                risk = "Low Risk"
            elif probability >= 0.50:
                risk = "Medium Risk"
            else:
                risk = "High Risk"

            st.metric(
                "Academic Risk",
                risk
            )

        # -------------------------------
        # Progress Bar
        # -------------------------------

        st.subheader("📈 Performance Probability")

        st.progress(float(probability))

        # -------------------------------
        # Personalized Suggestions
        # -------------------------------

        st.subheader("💡 Personalized Improvement Suggestions")

        suggestions = []

        if attendance < 75:
            suggestions.append(
                "🔴 Improve attendance to at least 75%."
            )

        if study_hours < 3:
            suggestions.append(
                "🔴 Increase daily study time to at least 3 hours."
            )

        if assignment_score < 60:
            suggestions.append(
                "🔴 Improve assignment scores and submit assignments on time."
            )

        if internal_marks < 60:
            suggestions.append(
                "🔴 Focus more on internal examinations."
            )

        if previous_gpa < 6:
            suggestions.append(
                "🔴 Improve academic consistency to increase GPA."
            )

        if participation < 5:
            suggestions.append(
                "🔴 Participate more actively in classroom activities."
            )

        if len(suggestions) == 0:
            suggestions.append(
                "🟢 Excellent! Keep maintaining your current performance."
            )

        for suggestion in suggestions:
            st.write(suggestion)

        # -------------------------------
        # Input Summary
        # -------------------------------

        st.divider()

        st.subheader("📋 Student Performance Summary")

        summary = pd.DataFrame({
            "Metric": [
                "Attendance",
                "Study Hours",
                "Assignment Score",
                "Internal Marks",
                "Previous GPA",
                "Participation"
            ],
            "Value": [
                f"{attendance}%",
                f"{study_hours} hours/day",
                f"{assignment_score}",
                f"{internal_marks}",
                f"{previous_gpa}",
                f"{participation}/10"
            ]
        })

        st.table(summary)