"""
Log Workout, register workout sessions, and track progress.
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from api_client import create_workout, delete_workout, get_workouts

st.set_page_config(page_title="Log Workout", layout="wide")
st.title("🏋️ Log Workout")

EXERCISE_TYPES = ["Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "Other"]

#======================================================
# FORM 
#======================================================

with st.form("workout_form", clear_on_submit=True):
    st.subheader("Log a new workout")
    col1, col2 = st.columns(2)

    with col1:
        workout_date = st.date_input("Date", value=date.today(), max_value=date.today())
        workout_type = st.selectbox("Workout Type", EXERCISE_TYPES)

    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=1440, value=45, step 5)
        calories = st.number_input("Calories Burned", min_value=0, max_value=10000, value=0, step=10)

    notes = st.text_area("Notes (optional)", placeholder="E.g. Felt great, need to improve form, etc.")
    submitted = st.form_submit_button("Log Workout", type="primary", use_container_width=True)

if submitted:
    try:
        create_workout(
            workout_date=workout_date,
            workout_type=workout_type,
            duration_minutes=duration,
            calories_burned=calories, if calories > 0 else None,
            notes=notes if notes else None,
        )
        st.success(f"{workout_type} ({duration} min) logged successfully!")
    except Exception as e:
        st.error(f"Error logging workout: {e}")

st.divider()

