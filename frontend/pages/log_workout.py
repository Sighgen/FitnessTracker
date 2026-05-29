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

#======================================================
# WORKOUT HISTORY
#======================================================

st.subheader("Workout History")

col_f1, col_f2 = st.columns(2)
with col_f1:
    filter_from = st.date_input("From date", value=date.today().replace(day=1))
with col_f2:
    filter_to = st.date_input("To date", value=date.today())

try:
    workouts = get_workouts(from_date=filter_from, to_date=filter_to)
except Exception as e:
    st.error(f"Error fetching workouts: {e}")
    st.stop()

if not workouts:
    st.info("No workouts logged in this period.")
else:
    df = pd.DataFrame(workouts)
    df = df.rename(columns={
        "date": "Date",
        "workout_type": "Type",
        "duration_minutes": "Minutes",
        "calories_burned": "Calories",
        "notes": "Notes",
    })
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    # Show table
    display_cols = ["Date", "Type", "Minutes", "Calories", "Notes"]
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

    # Delete
    st.subheader("Delete a workout")
    options = {f"{w['date']} — {w['workout_type']} ({w['duration_minutes']} min)": w["id"] for w in workouts}
    selected_label = st.selectbox("Select workout to delete", list(options.keys()))

    if st.button("Delete Workout", type="secondary"):
        try:
            delete_workout(workout_id=options[selected_label])
            st.success("Workout deleted successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error deleting workout: {e}")