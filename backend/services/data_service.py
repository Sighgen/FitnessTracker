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
WORKOUTS_FILE = DATA_DIR / "workouts.csv"
NUTRITION_FILE = DATA_DIR / "nutrition.csv"
WEIGHT_FILE = DATA_DIR / "weight.csv"
GOALS_FILE = DATA_DIR / "goals.csv"

# CSV schema definitions
WORKOUTS_SCHEMA = ["id", "date", "type", "duration_minutes", "calories_burned", "notes"]
NUTRITION_SCHEMA = ["date", "meal_name", "calories", "carbs", "protein", "fat"]
WEIGHT_SCHEMA = ["date", "weight_kg"]
GOALS_SCHEMA = ["id", "type", "target_value", "start_date", "end_date", "status"]

def ensure_data_directory() -> None:
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(exist_ok=True)
    for file, cols in [
        (WORKOUTS_FILE, WORKOUTS_COLS),
        (NUTRITION_FILE, NUTRITION_COLS),
        (WEIGHT_FILE, WEIGHT_COLS),
        (GOALS_FILE, GOALS_COLS),
    ]:
        if not file.exists():
            pd.DataFrame(columns=cols).to_csv(file, index=False)
    

def _generate_id() -> str:
    """Generate a unique ID for workouts and goals."""
    return str(uuid.uuid4())


def _load_csv(filepath: Path, cols: list[str]) -> pd.DataFrame:
    """Load CSV files into a DataFrame, ensuring the correct columns, if the file is empty."""
    _ensure_data_dir()
    df = pd.read_csv(filepath)
    if df.empty:
        return pd.DataFrame(columns=cols)
    return df

#####################################################
# Workout functions                                 #
#####################################################

def save_workout(entry: WorkoutEntry) -> WorkoutEntry:
    """Save a workout entry . retunrn generated id."""
    df = _load_csv(WORKOUTS_FILE, WORKOUTS_COlS)
    entry.id = _generate_id()
    new_row = pd.DataFrame([{
        "id": entry.id,
        "date": entry.date.isoformat(),
        "type": entry.type,
        "duration_minutes": entry.duration_minutes,
        "calories_burned": entry.calories_burned,
        "notes": entry.notes,
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(WORKOUTS_FILE, index=False)
    return entry
