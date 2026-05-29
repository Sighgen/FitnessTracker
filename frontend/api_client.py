"""
Shared API client, streamlit pages imported from here 
Handles communication with fastAPI backend
"""

import os
from datetime  import date
from typing import Any, Optional

import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")


def _get(path: str, params: Optional[dict] = None) -> Any:
    """Helper for GET requests to backend API."""
    r = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def _post(path: str, json: dict) -> Any:
    """Helper for POST requests to backend API."""
    r = requests.post(f"{BASE_URL}{path}", json=json, timeout=10)
    r.raise_for_status()
    return r.json()


def _delete(path: str) -> None:
    """Helper for DELETE requests to backend API."""
    r = requests.delete(f"{BASE_URL}{path}", timeout=10)
    r.raise_for_status()


    # =====================================================
    # WORKOUTS
    # =====================================================

    def get_workouts(from_date: Optional[date] = None, to_date: Optional[date] = None) -> list[dict]:
        """Fetch workouts from backend, optionally filtered by date range."""
        params = {}
        if from_date:
            params["from_date"] = str(from_date)
        if to_date:
            params["to_date"] = str(to_date)
        return _get("/workouts/", params=params)
    

    def create_workout(
            workout_date: date,
            workout_type: str,
            duration_minutes: int,
            calories_burned: Optional[int] = None,
            notes: Optional[str] = None,
    ) -> dict:
        return _post("/workouts/", {
            "date": str(workout_date),
            "workout_type": workout_type,
            "duration_minutes": duration_minutes,
            "calories_burned": calories_burned,
            "notes": notes,
        })
    
    def delete_workout(workout_id: int) -> None:
        _delete(f"/workouts/{workout_id}")


# =====================================================
# NUTRITION
# =====================================================

def get_nutrition(from_date: Optional[date] = None, to_date: Optional[date] = None) -> list[dict]:
    """Fetch nutrition entries from backend, optionally filtered by date range."""
    params = {}
    if from_date:
        params["from_date"] = str(from_date)
    if to_date:
        params["to_date"] = str(to_date)
    return _get("/nutrition/", params=params)

def create_nutrition(
        nutrition_date: date,
        meal_name: str,
        calories: int,
        protein: Optional[float] = None,
        carbs: Optional[float] = None,
        fats: Optional[float] = None,
) -> dict:
    return _post("/nutrition/", {
        "date": str(nutrition_date),
        "meal_name": meal_name,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fats": fats,
    })

def get_daily_calories(target_date: date) -> int:
    """Fetch total calories consumed for a specific date."""
    data = _get(f"/nutrition/daily/{target_date}")
    return data.get("total_calories")


# =====================================================
# WEIGHT
# =====================================================

def get_weight(from_date: Optional[date] = None, to_date: Optional[date] = None) -> list[dict]:
    """Fetch weight entries from backend, optionally filtered by date range."""
    params = {}
    if from_date:
        params["from_date"] = str(from_date)
    if to_date:
        params["to_date"] = str(to_date)
    return _get("/weight/", params=params)

def create_weight(weight_date: date, weight_kg: float) -> dict:
    return _post("/weight/", {"date": str(weight_date), "weight_kg": weight_kg})


# =====================================================
# STATS
# =====================================================

def get_workout_stats(days: int = 30) -> dict:
    """Fetch workout stats for the past N days."""
    return _get("/stats/workout/", params={"days": days})


def get_weight_stats(days: int = 30) -> dict:
    """Fetch weight stats for the past N days."""
    return _get("/stats/weight/", params={"days": days})