import pandas as pd
import pytest
from datetime import date, timedelta

from backend.services import data_service as ds


# -----------------------------
# Helpers: fake models
# -----------------------------
class FakeWorkout:
    def __init__(self):
        self.id = None
        self.date = date.today()
        self.type = "run"
        self.duration_minutes = 30
        self.calories_burned = 250
        self.notes = "morning run"


class FakeNutrition:
    def __init__(self):
        self.id = None
        self.date = date.today()
        self.meal_name = "breakfast"
        self.calories = 500
        self.carbs = 60
        self.protein = 20
        self.fat = 10


class FakeWeight:
    def __init__(self, w=80.0, d=None):
        self.id = None
        self.date = d or date.today()
        self.weight_kg = w


class FakeGoal:
    def __init__(self):
        self.goal_type = "loss"
        self.target_weight_kg = 75.0
        self.target_workout_minutes = 3
        self.target_calories = 2000
        self.notes = "test goal"

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    # redirect data directory
    monkeypatch.setattr(ds, "DATA_DIR", tmp_path)

    # update file paths
    monkeypatch.setattr(ds, "WORKOUTS_FILE", tmp_path / "workouts.csv")
    monkeypatch.setattr(ds, "NUTRITION_FILE", tmp_path / "nutrition.csv")
    monkeypatch.setattr(ds, "WEIGHT_FILE", tmp_path / "weight.csv")
    monkeypatch.setattr(ds, "GOALS_FILE", tmp_path / "goals.csv")

    ds.ensure_data_directory()
    yield


# -----------------------------
# WORKOUT TESTS
# -----------------------------

def test_save_and_get_workout():
    w = FakeWorkout()
    saved = ds.save_workout(w)

    assert saved.id is not None

    df = ds.get_workouts()
    assert len(df) == 1
    assert df.iloc[0]["type"] == "run"


def test_delete_workout():
    w = FakeWorkout()
    saved = ds.save_workout(w)

    assert ds.delete_workout(saved.id) is True
    assert ds.delete_workout("nonexistent") is False


# -----------------------------
# NUTRITION TESTS
# -----------------------------

def test_save_and_get_nutrition():
    n = FakeNutrition()
    saved = ds.save_nutrition(n)

    df = ds.get_nutrition()
    assert len(df) == 1
    assert df.iloc[0]["meal_name"] == "breakfast"


def test_daily_calories():
    n = FakeNutrition()
    ds.save_nutrition(n)

    total = ds.get_daily_calories(date.today())
    assert total == 500


def test_delete_nutrition():
    n = FakeNutrition()
    saved = ds.save_nutrition(n)

    assert ds.delete_nutrition(saved.id) is True
    assert ds.delete_nutrition("bad") is False


# -----------------------------
# WEIGHT TESTS
# -----------------------------

def test_save_and_get_weight():
    w = FakeWeight()
    ds.save_weight(w)

    df = ds.get_weight()
    assert len(df) == 1


def test_weight_trend():
    ds.save_weight(FakeWeight(80.0, date.today() - timedelta(days=2)))
    ds.save_weight(FakeWeight(79.0, date.today() - timedelta(days=1)))

    trend = ds.get_weight_stats(days=5)
    assert "trend" in trend
    assert trend["current_weight"] == 79.0


# -----------------------------
# STATS TESTS
# -----------------------------

def test_workout_stats():
    ds.save_workout(FakeWorkout())

    stats = ds.get_workout_stats(days=1)
    assert stats["total_workouts"] == 1


def test_nutrition_stats():
    ds.save_nutrition(FakeNutrition())

    stats = ds.get_nutrition_stats(days=1)
    assert stats["total_meals"] == 1


# -----------------------------
# GOALS TESTS
# -----------------------------

def test_save_and_get_goal():
    g = FakeGoal()
    ds.save_goal(g)

    goal = ds.get_goal()
    assert goal is not None
    assert goal.goal_type == "loss"
