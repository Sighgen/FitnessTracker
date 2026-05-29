"""
Data service module for handling data-related operations.

Saves data in CSV format and provides functions to read and write data.
Uses pandas for data manipulation and file handling.
"""

import uuid
from datetime import date
from pathlib import Path
from typing import Optional, Union

import pandas as pd

from backend.models import Goal, Nutrition, Weight, Workout


# -----------------------------
# Paths
# -----------------------------

DATA_DIR = Path("data")

WORKOUTS_FILE = DATA_DIR / "workouts.csv"
NUTRITION_FILE = DATA_DIR / "nutrition.csv"
WEIGHT_FILE = DATA_DIR / "weight.csv"
GOALS_FILE = DATA_DIR / "goals.csv"


# -----------------------------
# Schemas
# -----------------------------

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
    "goal_type",
    "target_weight_kg",
    "target_workout_minutes",
    "target_calories",
    "weekly_workouts",
    "daily_calorie_target",
    "notes",
]


# -----------------------------
# Setup
# -----------------------------


def ensure_data_directory() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    for file, cols in [
        (WORKOUTS_FILE, WORKOUTS_SCHEMA),
        (NUTRITION_FILE, NUTRITION_SCHEMA),
        (WEIGHT_FILE, WEIGHT_SCHEMA),
        (GOALS_FILE, GOALS_SCHEMA),
    ]:
        if (not file.exists()) or file.stat().st_size == 0:
            pd.DataFrame(columns=cols).to_csv(file, index=False)


def _generate_id() -> str:
    return str(uuid.uuid4())


def _load_csv(filepath: Path, cols: list[str]) -> pd.DataFrame:
    ensure_data_directory()

    if not filepath.exists() or filepath.stat().st_size == 0:
        return pd.DataFrame(columns=cols)

    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=cols)

    return df if not df.empty else pd.DataFrame(columns=cols)


def _filter_by_date(
    df: pd.DataFrame,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date

    if from_date:
        df = df[df["date"] >= from_date]

    if to_date:
        df = df[df["date"] <= to_date]

    return df.sort_values("date", ascending=False).reset_index(drop=True)


def _safe_float(value: Optional[Union[str, int, float]]) -> Optional[float]:
    """Safely convert values coming from CSV into float."""
    try:
        if value is None:
            return None
        parsed = float(value)
        return parsed if parsed >= 0 else None
    except (TypeError, ValueError):
        return None


# =====================================================
# WORKOUTS
# =====================================================


def save_workout(entry: Workout) -> Workout:
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
    df = _load_csv(WORKOUTS_FILE, WORKOUTS_SCHEMA)
    return _filter_by_date(df, from_date, to_date)


def delete_workout(workout_id: str) -> bool:
    df = _load_csv(WORKOUTS_FILE, WORKOUTS_SCHEMA)

    original_len = len(df)
    df = df[df["id"] != workout_id]

    if len(df) == original_len:
        return False

    df.to_csv(WORKOUTS_FILE, index=False)
    return True


# =====================================================
# NUTRITION
# =====================================================


def save_nutrition(entry: Nutrition) -> Nutrition:
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
    df = _load_csv(NUTRITION_FILE, NUTRITION_SCHEMA)
    return _filter_by_date(df, from_date, to_date)


def delete_nutrition(nutrition_id: str) -> bool:
    df = _load_csv(NUTRITION_FILE, NUTRITION_SCHEMA)

    original_len = len(df)
    df = df[df["id"] != nutrition_id]

    if len(df) == original_len:
        return False

    df.to_csv(NUTRITION_FILE, index=False)
    return True


def get_daily_calories(target_date: date) -> int:
    df = get_nutrition(from_date=target_date, to_date=target_date)

    if df.empty:
        return 0

    return int(df["calories"].sum())


# =====================================================
# WEIGHT
# =====================================================


def save_weight(entry: Weight) -> Weight:
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


def get_weight_entries(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> pd.DataFrame:
    """Get weight entries optionally filtered by date range."""

    df = _load_csv(WEIGHT_FILE, WEIGHT_SCHEMA)
    return _filter_by_date(df, from_date, to_date)


def delete_weight(weight_id: str) -> bool:
    df = _load_csv(WEIGHT_FILE, WEIGHT_SCHEMA)

    original_len = len(df)
    df = df[df["id"] != weight_id]

    if len(df) == original_len:
        return False

    df.to_csv(WEIGHT_FILE, index=False)
    return True


def get_weight_trend(from_date=None, to_date=None):
    df = _load_csv(WEIGHT_FILE, WEIGHT_SCHEMA)
    df = _filter_by_date(df, from_date, to_date)

    return df.iloc[::-1].reset_index(drop=True)


# =====================================================
# STATS
# =====================================================


def get_workout_stats(days: int = 30) -> dict:
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
        "average_calories": int(calories.mean()) if len(calories) else 0,
    }


def get_nutrition_stats(days: int = 30) -> dict:
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
        "average_calories": int(calories.mean()) if len(calories) else 0,
        "average_carbs": int(carbs.mean()) if len(carbs) else 0,
        "average_protein": int(protein.mean()) if len(protein) else 0,
        "average_fat": int(fat.mean()) if len(fat) else 0,
    }


def get_weight_stats(days: int = 30) -> dict:
    from_date = pd.Timestamp.now().date() - pd.Timedelta(days=days)

    df = get_weight_trend(from_date=from_date)

    if df.empty:
        return {
            "average_weight": 0.0,
            "weight_change": None,
            "weight_change_percentage": None,
            "current_weight": None,
            "trend": "no data",
        }

    weights = df["weight_kg"].astype(float).values

    current = float(weights[-1])
    start = float(weights[0])

    change = current - start
    pct = (change / start * 100) if start else None

    return {
        "average_weight": float(weights.mean()),
        "weight_change": change,
        "weight_change_percentage": pct,
        "current_weight": current,
        "trend": "down" if change < 0 else "up" if change > 0 else "stable",
    }


# =====================================================
# GOALS
# =====================================================


def save_goal(goal: Goal) -> Goal:
    goal.id = _generate_id()

    df = pd.DataFrame([{
        "id": goal.id,
        "goal_type": goal.goal_type,
        "target_weight_kg": goal.target_weight_kg,
        "target_workout_minutes": goal.target_workout_minutes,
        "target_calories": goal.target_calories,
        "weekly_workouts": goal.weekly_workouts,
        "daily_calorie_target": goal.daily_calorie_target,
        "notes": goal.notes,
    }])

    df.to_csv(GOALS_FILE, index=False)
    return goal


def get_goal() -> Optional[Goal]:
    df = _load_csv(GOALS_FILE, GOALS_SCHEMA)

    if df.empty:
        return None

    row = df.iloc[0]

    return Goal(
        goal_type=str(row["goal_type"]),
        target_weight_kg=(
            float(row["target_weight_kg"])
            if pd.notna(row["target_weight_kg"])
            else None
        ),
        target_workout_minutes=int(row["target_workout_minutes"]) if pd.notna(row["target_workout_minutes"]) else None,
        target_calories=(
            int(row["target_calories"]) if pd.notna(row["target_calories"]) else None
        ),
        weekly_workouts=int(row["weekly_workouts"]) if pd.notna(row["weekly_workouts"]) else 3,
        daily_calorie_target=int(row["daily_calorie_target"]) if pd.notna(row["daily_calorie_target"]) else None,
        notes=str(row["notes"]) if pd.notna(row["notes"]) else None,
    )