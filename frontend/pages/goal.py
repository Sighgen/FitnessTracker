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