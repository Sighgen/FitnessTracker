"""
Endpoints for workouts.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import sys
from pathlib import Path
sys.path.append(0, str(Path(__file__).parent.parent.parent))

from models import Workout
from services import data_service as ds

router = APIRouter(prefix="/workouts", tags=["workouts"])

class WorkoutIn(BaseModel):
    date: date
    workout_type: str = Field(..., min_length=1, example="Running")
    duration_minutes: int = Field(..., gt=0)
    calories_burned: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class WorkoutOut(WorkoutIn):
    id: str

@router.post("/", response_model=WorkoutOut, status_code=201)
def create_workout(workout: WorkoutIn) -> WorkoutOut:
    """Create a new workout entry."""
    try:
        entry = Workout(**body.model_dump())
        saved = ds.save_workout(entry)
        return WorkoutOut(**body.model_dump(), id=saved.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", response_model=list[WorkoutOut])
def list_workouts(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> list[WorkoutOut]:
    """List workouts, optionally filtered by date range."""
    df = ds.get_workouts(from_date=from_date, to_date=to_date)
    if df.empty:
        return []
    return [
        WorkoutOut(
            id=str(row["id"]),
            date=row["date"],
            workout_type=row["type"],
            duration_minutes=row["duration_minutes"],
            calories_burned=int(row["calories_burned"]) if row["calories_burned"] and str(row["calories_burned"]) != "nan" else None,
            notes=str(row["notes"]) if row["notes"] and str(row["notes"]) != "nan" else None,
        )
        for _, row in df.iterrows()
    ]


@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: str) -> None:
    """Delete a workout entry by ID."""
    if not ds.delete_workout(workout_id):
        raise HTTPException(status_code=404, detail="Workout not found")