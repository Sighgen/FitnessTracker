import pandas as pd
from datetime import date

from backend.services import data_service as ds
from backend.models import Workout, Nutrition, Weight


# =====================================================
# SETUP
# =====================================================

def setup_function():
    """Reset CSV files before each test."""
    ds.ensure_data_directory()

    # clean files
    for file in [
        ds.WORKOUTS_FILE,
        ds.NUTRITION_FILE,
        ds.WEIGHT_FILE,
        ds.GOALS_FILE,
    ]:
        pd.DataFrame().to_csv(file, index=False)


# =====================================================
# WORKOUT TESTS
# =====================================================

def test_save_and_get_workout():
    workout = Workout(
        date=date.today(),
        type="Running",
        duration_minutes=30,
        calories_burned=300,
        notes="Morning run",
    )

    saved = ds.save_workout(workout)

    df = ds.get_workouts()

    assert len(df) == 1
    assert df.iloc[0]["id"] == saved.id
    assert df.iloc[0]["type"] == "Running"


def test_delete_workout():
    workout = Workout(
        date=date.today(),
        type="Bike",
        duration_minutes=20,
    )

    saved = ds.save_workout(workout)

    result = ds.delete_workout(saved.id)

    assert result is True
    assert ds.get_workouts().empty is True


def test_delete_workout_not_found():
    result = ds.delete_workout("fake-id")
    assert result is False


# =====================================================
# WEIGHT TESTS
# =====================================================

def test_save_and_get_weight():
    weight = Weight(date=date.today(), weight_kg=80.5)

    saved = ds.save_weight(weight)

    df = ds.get_weight_entries()

    assert len(df) == 1
    assert df.iloc[0]["id"] == saved.id
    assert float(df.iloc[0]["weight_kg"]) == 80.5


def test_weight_trend():
    w1 = Weight(date=date.today(), weight_kg=80)
    w2 = Weight(date=date.today(), weight_kg=78)

    ds.save_weight(w1)
    ds.save_weight(w2)

    df = ds.get_weight_trend()

    assert len(df) == 2
    assert df.iloc[-1]["weight_kg"] == 80


# =====================================================
# NUTRITION TESTS
# =====================================================

def test_save_and_get_nutrition():
    n = Nutrition(
        date=date.today(),
        meal_name="Breakfast",
        calories=500,
        carbs=50,
        protein=20,
        fat=10,
    )

    saved = ds.save_nutrition(n)

    df = ds.get_nutrition()

    assert len(df) == 1
    assert df.iloc[0]["id"] == saved.id
    assert df.iloc[0]["meal_name"] == "Breakfast"


def test_daily_calories():
    n1 = Nutrition(date=date.today(), meal_name="A", calories=400)
    n2 = Nutrition(date=date.today(), meal_name="B", calories=600)

    ds.save_nutrition(n1)
    ds.save_nutrition(n2)

    total = ds.get_daily_calories(date.today())

    assert total == 1000


def test_empty_daily_calories():
    total = ds.get_daily_calories(date.today())
    assert total == 0


# =====================================================
# STATS TESTS
# =====================================================

def test_workout_stats_empty():
    stats = ds.get_workout_stats(days=1)

    assert stats["total_workouts"] == 0
    assert stats["total_duration"] == 0


def test_workout_stats():
    w = Workout(
        date=date.today(),
        type="Run",
        duration_minutes=60,
        calories_burned=500,
    )

    ds.save_workout(w)

    stats = ds.get_workout_stats(days=1)

    assert stats["total_workouts"] == 1
    assert stats["total_duration"] == 60
    assert stats["total_calories"] == 500