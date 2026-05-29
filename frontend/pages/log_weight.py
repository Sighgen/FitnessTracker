"""
Log weight
"""

import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from api_client import create_weight, get_weight, get_weight_stats

st.set_page_config(page_title="Log Weight", layout="wide")
st.title("⚖️ Log Weight")

#======================================================
# KEY NUMBERS
#======================================================

try:
    stats = get_weight_stats()
except Exception:
    stats = {"current_weight": None, "weight_change": None, "trend": "-", "average_weight": None}

col1, col2, col3 = st.columns(3)
col1.metric("Current Weight", f"{stats['current_weight']} kg" if stats["current_weight"] else "-")
col2.metric(
    "Change",
    f"{stats['weight_change']:+.1f} kg" if stats["weight_change"] else "-",
)
col3.metric("Trend", stats["trend", "-"])

st.divider()

#======================================================
# FORM
#======================================================

with st.form("weight_form", clear_on_submit=True):
    st.subheader("Log a new weight entry")
    col_a, col_b = st.columns(2)
    with col_a:
        weight_date = st.date_input("Date", value=date.today(), max_value=date.today())
    with col_b:
        weight_kg = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=70.0, step=0.1, format="%.1f")

    submitted = st.form_submit_button("Log Weight", type="primary", use_container_width=True)

if submitted:
    try:
        create_weight(weight_date=weight_date, weight_kg=weight_kg)
        st.success(f"Weight {weight_kg} kg logged {weight_date.strftime('%Y-%m-%d')}!")
    except Exception as e:
        st.error(f"Error logging weight: {e}")

st.divider()

#======================================================
# GRAPH
#======================================================

st.subheader("Weight History")

try:
    entries = get_weight()
except Exception as e:
    st.error(f"Error fetching weight history: {e}")
    st.stop()

if not entries:
    st.info("No weight entries logged yet.")
else:
    df = pd.DataFrame(entries)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["weight_kg"], marker="o", linewidth=2.5,
            color="#4f8ef7", markersize=6, label="Vægt")


    # Trend
    if len(df) >= 5:
        df["ma"] = df["weight_kg"].rolling(window=5, center=True).mean()
        ax.plot(df["date"], df["ma"], linewidth=1.5, linestyle="--", color="#f78c4f", alpha=0.8, label="Weighted Trend")
        ax.legend()

    ax.fill_between(df["date"], df["weight_kg"], df["weight_kg"].min() - 0.5, alpha=0.8, color="#4f8ef7")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()
    ax.set_ylabel("Weight (kg)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Table
    st.subheader("Weight Entries")
    df_display = df[["date", "weight_kg"]].copy()
    df_display["date"] = df_display["date"].dt.strftime("%Y-%m-%d")
    df_display = df_display.rename(columns={"date": "Date", "weight_kg": "Weight (kg)"})
    df_display = df_display.sort_values("Date", ascending=False)
    st.dataframe(df_display, use_container_width=True, hide_index=True)