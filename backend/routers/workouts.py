"""
Endpoints for workouts.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.models import Workout
from backend.services import data_service as ds

router = APIRouter(prefix="/workouts", tags=["workouts"])


class WorkoutIn(BaseModel):
    """Input model for workouts."""

    date: date
    workout_type: str = Field(..., min_length=1, example="Running")
    duration_minutes: int = Field(..., gt=0)
    calories_burned: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class WorkoutOut(WorkoutIn):
    """Output model for workouts."""

    id: str


def _safe_int(value) -> Optional[int]:
    """Safely convert values coming from pandas (handles NaN)."""
    try:
        if value is None:
            return None
        if str(value).lower() == "nan":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_str(value) -> Optional[str]:
    """Safely convert string fields from pandas."""
    if value is None:
        return None
    if str(value).lower() == "nan":
        return None
    return str(value)


@router.post("/", response_model=WorkoutOut, status_code=201)
def create_workout(workout: WorkoutIn) -> WorkoutOut:
    """Create a new workout entry."""

    try:
        entry = Workout(**workout.model_dump())
        saved = ds.save_workout(entry)

        return WorkoutOut(
            **workout.model_dump(),
            id=saved.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get("/", response_model=list[WorkoutOut])
def list_workouts(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> list[WorkoutOut]:
    """List workouts, optionally filtered by date range."""

    df = ds.get_workouts(
        from_date=from_date,
        to_date=to_date,
    )

    if df.empty:
        return []

    return [
        WorkoutOut(
            id=str(row["id"]),
            date=row["date"],
            workout_type=str(row["type"]),
            duration_minutes=int(row["duration_minutes"]),
            calories_burned=_safe_int(row["calories_burned"]),
            notes=_safe_str(row["notes"]),
        )
        for _, row in df.iterrows()
    ]


@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: str) -> None:
    """Delete a workout entry by ID."""

    if not ds.delete_workout(workout_id):
        raise HTTPException(
            status_code=404,
            detail="Workout not found",
        )
