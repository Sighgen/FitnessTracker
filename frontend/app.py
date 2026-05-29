"""
Simple FitTracker.
Streamlit frontend.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Simple FitTracker",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏋️‍♂️ Simple FitTracker")
st.markdown(
    """
    Welcome to Simple FitTracker!.

    Use the sidebar to navigate between pages:

    - **Dashboard**: View your workout and nutrition stats.
    - **Log Workout**: Log a new workout session.
    - **Log Nutrition**: Log your meals and calories.
    - **Log Weight**: Track your weight over time.
    - **AI Coach**: Get personalized workout and nutrition advice based on your data and goals.
    - **Set Goal**: Define your fitness goals to get tailored advice.
    """)

# Check backend
import requests
try:
    r = requests.get("http://localhost:8000/health", timeout=3)
    if r.status_code == 200:
        st.success("Backend is healthy and running!")
    else:
        st.error("Backend is running but returned an unexpected status code.")
except requests.ConnectionError:
    st.warning("Backend is not running. Please start the backend server to use all features.")