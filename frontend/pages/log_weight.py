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