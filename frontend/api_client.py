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