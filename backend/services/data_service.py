"""
Data service module for handling data-related operations.

Saves data in CSV format and provides functions to read and write data.
Uses pandas for data manipulation and file handling.
"""

import uuid
from datetime import date
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from models import Nutrition, Weight, Workout

# Path to the data directory
DATA_DIR = Path("data").parent / "data"

# CSV file paths
WORKOUTS_FILE = DATA_DIR / "workouts.csv"
NUTRITION_FILE = DATA_DIR / "nutrition.csv"
WEIGHT_FILE = DATA_DIR / "weight.csv"
GOALS_FILE = DATA_DIR / "goals.csv"

# CSV schema definitions
WORKOUTS_SCHEMA = [
    "id",
    "date",
    "type",
    "duration_minutes",
    "calories_burned",
    "notes",
]

NUTRITION_SCHEMA = [
    "id",
    "date",
    "meal_name",
    "calories",
    "carbs",
    "protein",
    "fat",
]

WEIGHT_SCHEMA = [
    "id",
    "date",
    "weight_kg",
]

GOALS_SCHEMA = [
    "id",
    "type",
    "target_value",
    "start_date",
    "end_date",
    "status",
]


def ensure_data_directory() -> None:
    """Ensure the data directory and CSV files exist."""
    DATA_DIR.mkdir(exist_ok=True)

    for file, cols in [
        (WORKOUTS_FILE, WORKOUTS_SCHEMA),
        (NUTRITION_FILE, NUTRITION_SCHEMA),
        (WEIGHT_FILE, WEIGHT_SCHEMA),
        (GOALS_FILE, GOALS_SCHEMA),
    ]:
        if not file.exists():
            pd.DataFrame(columns=cols).to_csv(file, index=False)


def _generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())


def _load_csv(filepath: Path, cols: list[str]) -> pd.DataFrame:
    """Load CSV file into a DataFrame."""
    ensure_data_directory()

    df = pd.read_csv(filepath)

    if df.empty:
        return pd.DataFrame(columns=cols)

    return df


######################################################
# Helper functions                                   #
######################################################


def _filter_by_date(
    df: pd.DataFrame,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> pd.DataFrame:
    """Filter DataFrame by optional date range."""
    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"]).dt.date

    if from_date:
        df = df[df["date"] >= from_date]

    if to_date:
        df = df[df["date"] <= to_date]

    return df.sort_values("date", ascending=False).reset_index(drop=True)


######################################################
# Workout functions                                  #
######################################################


def save_workout(entry: Workout) -> Workout:
    """Save a workout entry and return it with generated ID."""
    df = _load_csv(WORKOUTS_FILE, WORKOUTS_SCHEMA)

    entry.id = _generate_id()

    new_row = pd.DataFrame(
        [
            {
                "id": entry.id,
                "date": entry.date.isoformat(),
                "type": entry.type,
                "duration_minutes": entry.duration_minutes,
                "calories_burned": entry.calories_burned,
                "notes": entry.notes,
            }
        ]
    )

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(WORKOUTS_FILE, index=False)

    return entry


def get_workouts(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> pd.DataFrame:
    """Get workouts filtered by optional date range."""
    df = _load_csv(WORKOUTS_FILE, WORKOUTS_SCHEMA)

    return _filter_by_date(df, from_date, to_date)


def delete_workout(workout_id: str) -> bool:
    """Delete a workout by ID."""
    df = _load_csv(WORKOUTS_FILE, WORKOUTS_SCHEMA)

    original_len = len(df)

    df = df[df["id"] != workout_id]

    if len(df) == original_len:
        return False

    df.to_csv(WORKOUTS_FILE, index=False)

    return True


######################################################
# Nutrition functions                                #
######################################################


def save_nutrition(entry: Nutrition) -> Nutrition:
    """Save nutrition entry and return it with generated ID."""
    df = _load_csv(NUTRITION_FILE, NUTRITION_SCHEMA)

    entry.id = _generate_id()

    new_row = pd.DataFrame(
        [
            {
                "id": entry.id,
                "date": entry.date.isoformat(),
                "meal_name": entry.meal_name,
                "calories": entry.calories,
                "carbs": entry.carbs,
                "protein": entry.protein,
                "fat": entry.fat,
            }
        ]
    )

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(NUTRITION_FILE, index=False)

    return entry


def get_nutrition(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> pd.DataFrame:
    """Get nutrition entries filtered by optional date range."""
    df = _load_csv(NUTRITION_FILE, NUTRITION_SCHEMA)

    return _filter_by_date(df, from_date, to_date)


def delete_nutrition(nutrition_id: str) -> bool:
    """Delete a nutrition entry by ID."""
    df = _load_csv(NUTRITION_FILE, NUTRITION_SCHEMA)

    original_len = len(df)

    df = df[df["id"] != nutrition_id]

    if len(df) == original_len:
        return False

    df.to_csv(NUTRITION_FILE, index=False)

    return True


def get_daily_calories(target_date: date) -> int:
    """Calculate total calories consumed on a specific date."""
    df = get_nutrition(from_date=target_date, to_date=target_date)

    if df.empty:
        return 0

    return int(df["calories"].sum())


######################################################
# Weight functions                                   #
######################################################


def save_weight(entry: Weight) -> Weight:
    """Save weight entry."""
    df = _load_csv(WEIGHT_FILE, WEIGHT_SCHEMA)

    entry.id = _generate_id()

    new_row = pd.DataFrame(
        [
            {
                "id": entry.id,
                "date": entry.date.isoformat(),
                "weight_kg": entry.weight_kg,
            }
        ]
    )

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(WEIGHT_FILE, index=False)

    return entry


def get_weight(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> pd.DataFrame:
    """Get weight entries filtered by optional date range."""
    df = _load_csv(WEIGHT_FILE, WEIGHT_SCHEMA)

    return _filter_by_date(df, from_date, to_date)


def delete_weight(weight_id: str) -> bool:
    """Delete a weight entry by ID."""
    df = _load_csv(WEIGHT_FILE, WEIGHT_SCHEMA)

    original_len = len(df)

    df = df[df["id"] != weight_id]

    if len(df) == original_len:
        return False

    df.to_csv(WEIGHT_FILE, index=False)

    return True


def get_weight_trend(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> pd.DataFrame:
    """Get weight trend filtered by optional date range."""
    df = _load_csv(WEIGHT_FILE, WEIGHT_SCHEMA)

    return (
        _filter_by_date(df, from_date, to_date)
        .sort_values("date")
        .reset_index(drop=True)
    )


######################################################
# Stats functions                                    #
######################################################


def get_workout_stats(days: int = 30) -> dict:
    """
    Calculate workout stats for the past N days.

    Return dict with key numbers.
    """
    from_date = pd.Timestamp.now().date() - pd.Timedelta(days=days)

    df = get_workouts(from_date=from_date)

    if df.empty:
        return {
            "total_workouts": 0,
            "total_duration": 0,
            "total_calories": 0,
            "average_duration": 0,
            "average_calories": 0,
        }

    duration = df["duration_minutes"].astype(float).values
    calories = df["calories_burned"].dropna().astype(float).values

    return {
        "total_workouts": len(df),
        "total_duration": int(duration.sum()),
        "total_calories": int(calories.sum()),
        "average_duration": int(duration.mean()),
        "average_calories": int(calories.mean()) if len(calories) > 0 else 0,
    }


def get_nutrition_stats(days: int = 30) -> dict:
    """
    Calculate nutrition stats for the past N days.

    Return dict with key numbers.
    """
    from_date = pd.Timestamp.now().date() - pd.Timedelta(days=days)

    df = get_nutrition(from_date=from_date)

    if df.empty:
        return {
            "total_meals": 0,
            "total_calories": 0,
            "average_calories": 0,
            "average_carbs": 0,
            "average_protein": 0,
            "average_fat": 0,
        }

    calories = df["calories"].dropna().astype(float).values
    carbs = df["carbs"].dropna().astype(float).values
    protein = df["protein"].dropna().astype(float).values
    fat = df["fat"].dropna().astype(float).values

    return {
        "total_meals": len(df),
        "total_calories": int(calories.sum()),
        "average_calories": int(calories.mean()) if len(calories) > 0 else 0,
        "average_carbs": int(carbs.mean()) if len(carbs) > 0 else 0,
        "average_protein": int(protein.mean()) if len(protein) > 0 else 0,
        "average_fat": int(fat.mean()) if len(fat) > 0 else 0,
    }


def get_weight_stats(days: int = 30) -> dict:
    """Calculate weight statistics."""
    from_date = pd.Timestamp.now().date() - pd.Timedelta(days=days)

    df = get_weight_trend(from_date=from_date)

    if df.empty or len(df) < 2:
        current = float(df["weight_kg"].iloc[-1]) if not df.empty else None

        return {
            "current_weight": current,
            "start_weight": current,
            "change": 0.0,
            "trend": "not enough data",
        }

    weights = df["weight_kg"].dropna().astype(float).values

    change = round(float(weights[-1]) - float(weights[0]), 1)

    # Simple trend analysis with NumPy polyfit
    x = np.arange(len(weights))

    slope, _ = np.polyfit(x, weights, 1)

    trend = "down" if slope < -0.05 else "up" if slope > 0.05 else "stable"

    return {
        "current_weight": round(float(weights[-1]), 1),
        "start_weight": round(float(weights[0]), 1),
        "change": change,
        "trend": trend,
    }

#######################################################
# User goal functions                                 #
#######################################################

def save_goal(goal: UserGoal) -> UserGoal:
    """Save a users goal (overwrite existing goal)."""
    _ensure_data_dir()
    df = pd.DataFrame(
        [
            {
                "goal_type": goal.goal_type,
                "target_weight": goal.target_weight,
                "weekly_workouts": goal.weekly_workouts,
                "daily_calories": goal.daily_calories,
                "notes": goal.notes,
            }
        ]
    )
    df.to_csv(GOALS_FILE, index=False)
    return goal

def get_goal() -> Optional[UserGoal]:
    """Get user's goal (return None if not set)."""
    df = _load_csv(GOALS_FILE, GOALS_SCHEMA)
    if df.empty:
        return None
    row = df.iloc[0]
    return UserGoal(
        goal_type=str(row["goal_type"]),
        target_weight=float(row["target_weight"]) if pd.notna(row["target_weight"]) else None,
        weekly_workouts=int(row["weekly_workouts"]),
        daily_calories=int(row["daily_calories"]) if pd.notna(row["daily_calories"]) else None,
        notes=str(row["notes"]) if pd.notna(row["notes"]) else None,
    )