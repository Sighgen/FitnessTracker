import pytest
from datetime import date

from backend.services import data_service as ds
from backend.models import Workout, Nutrition, Weight


# =====================================================
# SETUP — isolate CSV files per test
# =====================================================

@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    """Redirect all CSV paths to a temporary directory so tests never
    touch the real data/ folder and can't interfere with each other."""
    monkeypatch.setattr(ds, "DATA_DIR", tmp_path)
    monkeypatch.setattr(ds, "WORKOUTS_FILE", tmp_path / "workouts.csv")
    monkeypatch.setattr(ds, "NUTRITION_FILE", tmp_path / "nutrition.csv")
    monkeypatch.setattr(ds, "WEIGHT_FILE", tmp_path / "weight.csv")
    monkeypatch.setattr(ds, "GOALS_FILE", tmp_path / "goals.csv")


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
    workout = Workout(date=date.today(), type="Bike", duration_minutes=20)
    saved = ds.save_workout(workout)

    assert ds.delete_workout(saved.id) is True
    assert ds.get_workouts().empty is True


def test_delete_workout_not_found():
    assert ds.delete_workout("fake-id") is False


def test_workout_negative_duration_raises():
    with pytest.raises(ValueError, match="positive"):
        Workout(date=date.today(), type="Running", duration_minutes=-5)


def test_workout_zero_duration_raises():
    with pytest.raises(ValueError):
        Workout(date=date.today(), type="Running", duration_minutes=0)


# =====================================================
# WEIGHT TESTS
# =====================================================

def test_save_and_get_weight():
    weight = Weight(date=date.today(), weight_kg=80.5)
    saved = ds.save_weight(weight)
    df = ds.get_weight_entries()

    assert len(df) == 1
    assert df.iloc[0]["id"] == saved.id
    assert float(df.iloc[0]["weight_kg"]) == pytest.approx(80.5)


def test_weight_trend():
    ds.save_weight(Weight(date=date.today(), weight_kg=80))
    ds.save_weight(Weight(date=date.today(), weight_kg=78))
    df = ds.get_weight_trend()

    assert len(df) == 2
    assert df.iloc[-1]["weight_kg"] == 80


def test_delete_weight():
    saved = ds.save_weight(Weight(date=date.today(), weight_kg=80.0))
    assert ds.delete_weight(saved.id) is True
    assert ds.get_weight_entries().empty is True


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
    ds.save_nutrition(Nutrition(date=date.today(), meal_name="A", calories=400))
    ds.save_nutrition(Nutrition(date=date.today(), meal_name="B", calories=600))

    assert ds.get_daily_calories(date.today()) == 1000


def test_empty_daily_calories():
    assert ds.get_daily_calories(date.today()) == 0


def test_daily_calories_only_counts_target_date():
    from datetime import timedelta
    yesterday = date.today() - timedelta(days=1)
    ds.save_nutrition(Nutrition(date=yesterday, meal_name="A", calories=999))
    ds.save_nutrition(Nutrition(date=date.today(), meal_name="B", calories=400))

    assert ds.get_daily_calories(date.today()) == 400


def test_delete_nutrition():
    saved = ds.save_nutrition(Nutrition(date=date.today(), meal_name="snack", calories=200))
    assert ds.delete_nutrition(saved.id) is True
    assert ds.get_nutrition().empty is True


# =====================================================
# STATS TESTS
# =====================================================

def test_workout_stats_empty():
    stats = ds.get_workout_stats(days=1)
    assert stats["total_workouts"] == 0
    assert stats["total_duration"] == 0


def test_workout_stats():
    ds.save_workout(Workout(date=date.today(), type="Run", duration_minutes=60, calories_burned=500))
    stats = ds.get_workout_stats(days=1)

    assert stats["total_workouts"] == 1
    assert stats["total_duration"] == 60
    assert stats["total_calories"] == 500


def test_workout_stats_excludes_old_entries():
    from datetime import timedelta
    old = date.today() - timedelta(days=60)
    ds.save_workout(Workout(date=old, type="Run", duration_minutes=60))
    stats = ds.get_workout_stats(days=30)

    assert stats["total_workouts"] == 0


def test_weight_stats_empty():
    stats = ds.get_weight_stats()
    assert stats["current_weight"] is None
    assert stats["trend"] == "no data"


def test_weight_stats_downward_trend():
    from datetime import timedelta
    for i, kg in enumerate([85.0, 84.0, 83.0, 82.0, 81.0]):
        ds.save_weight(Weight(date=date.today() - timedelta(days=20 - i * 4), weight_kg=kg))

    stats = ds.get_weight_stats()
    assert stats["trend"] == "down"
    assert stats["current_weight"] == pytest.approx(81.0)