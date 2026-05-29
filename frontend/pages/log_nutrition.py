"""
Log nutrition page
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from api_client import create_nutrition, get_nutrition, get_daily_calories

st.set_page_config(page_title="Log Nutrition", layout="wide")
st.title("🍎 Log Nutrition")

MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snack"]

#======================================================
# DAILY OVERVIEW
#======================================================

try:
    calories = get_daily_calories(date.today())
except Exception:
    today_calories = 0

st.metric("Today's Calories", f"{today_calories} kcal")
st.divider()