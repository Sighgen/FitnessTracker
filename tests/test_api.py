"""
API integration tests for all FastAPI endpoints.
Uses FastAPI's TestClient — no running server needed.

Run with: pytest tests/test_api.py -v
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))

import backend.services.data_service as ds
from backend.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    """Isolate CSV files per test — never touches real data/."""
    monkeypatch.setattr(ds, "DATA_DIR", tmp_path)
    monkeypatch.setattr(ds, "WORKOUTS_FILE", tmp_path / "workouts.csv")
    monkeypatch.setattr(ds, "NUTRITION_FILE", tmp_path / "nutrition.csv")
    monkeypatch.setattr(ds, "WEIGHT_FILE", tmp_path / "weight.csv")
    monkeypatch.setattr(ds, "GOALS_FILE", tmp_path / "goals.csv")


# =====================================================
# STATUS
# =====================================================

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# =====================================================
# WORKOUTS
# =====================================================

class TestWorkoutsAPI:
    def test_create_workout(self):
        r = client.post("/workouts/", json={
            "date": "2024-03-01",
            "workout_type": "Running",
            "duration_minutes": 45,
            "calories_burned": 400,
        })
        assert r.status_code == 201
        data = r.json()
        assert data["workout_type"] == "Running"
        assert data["duration_minutes"] == 45
        assert "id" in data

    def test_create_workout_invalid_duration(self):
        r = client.post("/workouts/", json={
            "date": "2024-03-01",
            "workout_type": "Running",
            "duration_minutes": 0,
        })
        assert r.status_code == 422

    def test_create_workout_negative_duration(self):
        r = client.post("/workouts/", json={
            "date": "2024-03-01",
            "workout_type": "Running",
            "duration_minutes": -10,
        })
        assert r.status_code == 422

    def test_list_workouts_empty(self):
        r = client.get("/workouts/")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_workouts(self):
        client.post("/workouts/", json={"date": "2024-03-01", "workout_type": "Running", "duration_minutes": 30})
        client.post("/workouts/", json={"date": "2024-03-02", "workout_type": "Yoga", "duration_minutes": 60})
        r = client.get("/workouts/")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_list_workouts_date_filter(self):
        client.post("/workouts/", json={"date": "2024-01-01", "workout_type": "Running", "duration_minutes": 30})
        client.post("/workouts/", json={"date": "2024-06-01", "workout_type": "Running", "duration_minutes": 30})
        r = client.get("/workouts/?from_date=2024-06-01")
        assert len(r.json()) == 1

    def test_delete_workout(self):
        r = client.post("/workouts/", json={"date": "2024-03-01", "workout_type": "Running", "duration_minutes": 30})
        workout_id = r.json()["id"]
        r = client.delete(f"/workouts/{workout_id}")
        assert r.status_code == 204
        assert client.get("/workouts/").json() == []

    def test_delete_nonexistent_workout(self):
        r = client.delete("/workouts/does-not-exist")
        assert r.status_code == 404


# =====================================================
# NUTRITION
# =====================================================

class TestNutritionAPI:
    def test_create_nutrition(self):
        r = client.post("/nutrition/", json={
            "date": "2024-03-01",
            "meal_name": "Lunch",
            "calories": 650,
            "protein": 30,
            "carbs": 80,
            "fat": 20,
        })
        assert r.status_code == 201
        data = r.json()
        assert data["calories"] == 650
        assert "id" in data

    def test_create_nutrition_negative_calories(self):
        r = client.post("/nutrition/", json={
            "date": "2024-03-01",
            "meal_name": "snack",
            "calories": -50,
        })
        assert r.status_code == 422

    def test_list_nutrition_empty(self):
        r = client.get("/nutrition/")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_nutrition(self):
        client.post("/nutrition/", json={"date": "2024-03-01", "meal_name": "Breakfast", "calories": 400})
        client.post("/nutrition/", json={"date": "2024-03-01", "meal_name": "Lunch", "calories": 600})
        r = client.get("/nutrition/")
        assert len(r.json()) == 2

    def test_daily_calories(self):
        for meal, kcal in [("Breakfast", 400), ("Lunch", 600), ("Dinner", 700)]:
            client.post("/nutrition/", json={"date": "2024-03-01", "meal_name": meal, "calories": kcal})
        r = client.get("/nutrition/daily/2024-03-01")
        assert r.status_code == 200
        assert r.json()["total_calories"] == 1700

    def test_daily_calories_empty_day(self):
        r = client.get("/nutrition/daily/2024-01-01")
        assert r.status_code == 200
        assert r.json()["total_calories"] == 0


# =====================================================
# WEIGHT
# =====================================================

class TestWeightAPI:
    def test_create_weight(self):
        r = client.post("/weight/", json={"date": "2024-03-01", "weight_kg": 82.5})
        assert r.status_code == 201
        assert r.json()["weight_kg"] == pytest.approx(82.5)
        assert "id" in r.json()

    def test_create_weight_invalid(self):
        r = client.post("/weight/", json={"date": "2024-03-01", "weight_kg": -5})
        assert r.status_code == 422

    def test_list_weight_empty(self):
        r = client.get("/weight/")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_weight(self):
        client.post("/weight/", json={"date": "2024-03-01", "weight_kg": 83.0})
        client.post("/weight/", json={"date": "2024-03-10", "weight_kg": 82.0})
        r = client.get("/weight/")
        assert len(r.json()) == 2


# =====================================================
# STATS
# =====================================================

class TestStatsAPI:
    def test_workout_stats_empty(self):
        r = client.get("/stats/workouts")
        assert r.status_code == 200
        data = r.json()
        assert data["total_workouts"] == 0
        assert data["total_duration"] == 0

    def test_workout_stats_with_data(self):
        today = date.today().isoformat()
        client.post("/workouts/", json={"date": today, "workout_type": "Running", "duration_minutes": 30, "calories_burned": 300})
        client.post("/workouts/", json={"date": today, "workout_type": "Running", "duration_minutes": 60, "calories_burned": 500})
        r = client.get("/stats/workouts?days=1")
        data = r.json()
        assert data["total_workouts"] == 2
        assert data["total_duration"] == 90
        assert data["total_calories"] == 800

    def test_weight_stats_empty(self):
        r = client.get("/stats/weight")
        assert r.status_code == 200
        assert r.json()["current_weight"] is None
        assert r.json()["trend"] == "no data"

    def test_weight_stats_with_data(self):
        for i, kg in enumerate([85.0, 83.0, 81.0]):
            d = (date.today() - timedelta(days=20 - i * 7)).isoformat()
            client.post("/weight/", json={"date": d, "weight_kg": kg})
        r = client.get("/stats/weight?days=30")
        data = r.json()
        assert data["trend"] == "down"
        assert data["current_weight"] == pytest.approx(81.0)


# =====================================================
# GOALS
# =====================================================

class TestGoalsAPI:
    def test_save_and_get_goal(self):
        r = client.post("/goals", json={
            "goal_type": "weight_loss",
            "target_weight_kg": 75.0,
            "weekly_workouts": 4,
            "daily_calorie_target": 2000,
        })
        assert r.status_code == 201

        r = client.get("/goals")
        assert r.status_code == 200
        data = r.json()
        assert data["goal_type"] == "weight_loss"
        assert data["weekly_workouts"] == 4
        assert data["daily_calorie_target"] == 2000

    def test_get_goal_not_found(self):
        r = client.get("/goals")
        assert r.status_code == 404

    def test_overwrite_goal(self):
        client.post("/goals", json={"goal_type": "weight_loss", "weekly_workouts": 3})
        client.post("/goals", json={"goal_type": "muscle_gain", "weekly_workouts": 5})
        r = client.get("/goals")
        assert r.json()["goal_type"] == "muscle_gain"