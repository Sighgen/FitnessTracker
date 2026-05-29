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