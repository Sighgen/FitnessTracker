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

    