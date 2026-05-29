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

#======================================================
# FORM
#======================================================

with st.form("nutrition_form", clear_on_submit=True):
    st.subheader("Log a new meal")
    col1, col2 = st.columns(2)

    with col1:
        nutrition_date = st.date_input("Date", value=date.today(), max_value=date.today())
        meal_name = st.text_selectbox("Meal Type", MEAL_TYPES)
        calories = st.number_input("Calories (kcal)", min_value=0, max_value=10000, value=500, step=10)

    with col2:
        protein = st.number_input("Protein (g)", min_value=0, max_value=1000, value=25, step=1)
        carbs = st.number_input("Carbs (g)", min_value=0, max_value=1000, value=50, step=1)
        fats = st.number_input("Fats (g)", min_value=0, max_value=1000, value=20, step=1)

    submitted = st.form_submit_button("Log Meal", type="primary", use_container_width=True)

if submitted:
    try:
        create_nutrition(
            nutrition_date=nutrition_date,
            meal_name=meal_name,
            calories=calories,
            protein=protein if protein > 0 else None,
            carbs=carbs if carbs > 0 else None,
            fats=fats if fats > 0 else None,
        )
        st.success(f"{meal_name} ({calories} kcal) logged successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Error logging meal: {e}")

st.divider()