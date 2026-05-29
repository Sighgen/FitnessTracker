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

#======================================================
# KEY NUMBERS
#======================================================

try:
    workout_stats = get_workout_stats(days=days)
    weight_stats = get_weight_stats(days=days)
    calories = get_daily_calories(date.today())
except Exception as e:
    st.error(f"Error fetching stats: {e}")
    st.stop()

st.subheader("Key Metrics")
k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Workouts",
    workout_stats["total_workouts"],
    help=f"Latest {days} days",
)
k2.metric(
    "Total Workout Duration",
    f"{workout_stats['total_duration']} min",       # fix: total_duration_minutes → total_duration
    help=f"Latest {days} days",
)
k3.metric(
    "Current Weight",
    f"{weight_stats['current_weight']} kg" if weight_stats["current_weight"] else "-",
    delta=f"{weight_stats['weight_change']:+.1f} kg" if weight_stats.get("weight_change") else None,
)                                                   # fix: current_weight_kg → current_weight
k4.metric(
    "Today's Calories",
    f"{calories} kcal",                             # fix: today_calories → calories
)

st.divider()

#======================================================
# GRAPHS
#======================================================

col1, col2 = st.columns(2)

# Weight graph
with col1:
    st.subheader("Weight Over Time")
    weight_data = get_weight(from_date=from_date)

    if weight_data:
        df = pd.DataFrame(weight_data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(df["date"], df["weight_kg"], marker="o", linewidth=2,
                color="#4f8ef7", markersize=5)
        ax.fill_between(df["date"], df["weight_kg"],
                        df["weight_kg"].min() - 0.5, alpha=0.1, color="#4f8ef7")  # fix: syntaksfejl
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate()
        ax.set_ylabel("Weight (kg)")
        ax.set_xlabel("")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No weight data available.")

# Workout graph
with col2:
    st.subheader("Workout sessions")
    workout_data = get_workouts(from_date=from_date)

    if workout_data:
        df = pd.DataFrame(workout_data)
        df["date"] = pd.to_datetime(df["date"])

        # Group per week
        df["week"] = df["date"].dt.to_period("W").apply(lambda p: p.start_time)
        weekly = df.groupby("week").size().reset_index(name="count")

        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.bar(weekly["week"], weekly["count"], color="#34c88a", width=5, alpha=0.85)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate()
        ax.set_ylabel("Number of workouts")
        ax.set_xlabel("Week start date")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No workout data available.")

st.divider()
col3, col4 = st.columns(2)

# Calories over time
with col3:
    st.subheader("Calorie intake")
    nutrition_data = get_nutrition(from_date=from_date)

    if nutrition_data:
        df = pd.DataFrame(nutrition_data)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        daily = df.groupby("date")["calories"].sum().reset_index()
        daily["date"] = pd.to_datetime(daily["date"])

        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.bar(daily["date"], daily["calories"], color="#f7874f", alpha=0.85, width=0.8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate()
        ax.set_ylabel("Calories (kcal)")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No nutrition data available.")

# Workout types
with col4:
    st.subheader("Workout types")
    workout_data = workout_data if "workout_data" in dir() else get_workouts(from_date=from_date)

    if workout_data:
        df = pd.DataFrame(workout_data)
        type_counts = df["workout_type"].value_counts()

        fig, ax = plt.subplots(figsize=(6, 3.5))
        wedges, texts, autotexts = ax.pie(
            type_counts.values,
            labels=type_counts.index,
            autopct="%1.1f%%",
            colors=["#4f8ef7", "#34c88a", "#f7874f", "#f7c84f", "#9b59b6"],
            startangle=90,
        )
        for text in autotexts:
            text.set_fontsize(9)
        ax.set_title("")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No workout data available.")