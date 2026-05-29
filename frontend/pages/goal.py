"""
Goal page
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from api_client import get_goal, save_goal

st.set_page_config(page_title="Set Goal", layout="wide")
st.title("🎯 Set Your Fitness Goal")

GOAL_TYPES = {
    "weight_loss": "Weight Loss",
    "muscle_gain": "Muscle Gain",
    "endurance": "Endurance",
    "maintenance": "Maintenance",
    "general_fitness": "General Fitness",
}

#======================================================
# FETCH EXISTING GOAL
#======================================================

try:
    existing = get_goal()
except Exception:
    existing = None

if existing:
    st.success("Existing goal loaded. Update the form below to change it.")
    st.markdown(f"""
    **Current goal:** {GOAL_TYPES.get(existing['goal_type'], existing['goal_type'])}
    · **Weekly workouts:** {existing.get('weekly_workouts', '–')}
    · **Daily calorie intake:** {existing.get('daily_calorie_target') or '–'} kcal
    """)
st.divider()

#======================================================
# FORM
#======================================================

st.subheader("Set or Update Your Goal")


# Set default values from existing goal
default_goal_idx = list(GOAL_TYPES.keys()).index(existing["goal_type"]) if existing and existing.get("goal_type") in GOAL_TYPES else 0
default_weekly = existing.get("weekly_workouts", 3) if existing else 3
default_target_weight = existing.get("target_weight_kg") or 0.0 if existing else 0.0
default_calorie = existing.get("daily_calorie_target") or 0 if existing else 0
default_notes = existing.get("notes", "") if existing else ""

with st.form("goal_form"):
    col1, col2 = st.columns(2)

    with col1:
        goal_type = st.selectbox(
            "What is your primary fitness goal?",
            options=list(GOAL_TYPES.keys()),
            format_func=lambda x: GOAL_TYPES[x],
            index=default_goal_idx,
        )
        weekly_workouts = st.slider(
            "How many workouts per week do you aim for?",
            min_value=1,
            max_value=14,
            value=default_weekly,
        )

    with col2:
        target_weight = st.number_input(
            "Target weight (kg, optional)",
            min_value=0.0, max_value=500.0,
            value=float(default_target_weight),
            step=0.5, format="%.1f"
        )
        daily_calorie_target = st.number_input(
            "Daily calorie intake target (kcal, optional)",
            min_value=0, max_value=10000,
            value=int(default_calorie),
            step=50
        )

    notes = st.text_area("Additional notes (optional)", value=default_notes, height=80)

    submitted = st.form_submit_button("Save Goal", type="primary", use_container_width=True)

if submitted:
    try:
        save_goal(
            goal_type=goal_type,
            weekly_workouts=weekly_workouts,
            target_weight_kg=target_weight if target_weight > 0 else None,
            daily_calorie_target=daily_calorie_target if daily_calorie_target > 0 else None,
            notes=notes if notes else None,
        )
        st.success("Goal saved successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Error saving goal: {e}")

st.divider()
st.caption("Your fitness goal helps you stay focused and track your progress. Update it anytime as your priorities evolve!")