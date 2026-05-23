"""
Data service module for handling data-related operations.
Saves in CSV format and provides functions to read and write data.
Uses pandas for data manipulation and file handling and NumPy for numerical computations.
"""

import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from models import Workout, Nutrition, Weight, Goal

# Path to the data directory
DATA_DIR = Path("data").parent / "data"

# CSV file paths
WORKOUTS_CSV = DATA_DIR / "workouts.csv"
NUTRITION_CSV = DATA_DIR / "nutrition.csv"
WEIGHT_CSV = DATA_DIR / "weight.csv"
GOALS_CSV = DATA_DIR / "goals.csv"

