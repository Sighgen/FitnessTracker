"""
Dashboard, shows statistics and charts about the user's fitness data.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from api_client import (
    get_weight,
    get_workout_stats,
    get_weight_stats,
    get_workouts,
    get_nutrition,
    get_daily_calories,
)

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Fitness Dashboard")

#======================================================
# DATE
#======================================================

col_l, col_r = st.columns([2, 1])
with col_r:
    days_options = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}
    selected = st.selectbox("Select time range", list(days_options.keys()), index=1)
    days = days_options[selected]

from_date = date.today() - timedelta(days=days)