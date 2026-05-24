"""
Endpoints for stats.
"""

import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Goal
from services import data_service as ds

router = APIRouter(tags=["stats"])


# ------------------------------------------------------------------
# Stats output models
# ------------------------------------------------------------------


class WorkoutStatsOut(BaseModel):
    """Output model for workout statistics."""

    total_workouts: int
    total_duration_minutes: int
    total_calories_burned: Optional[int] = None
    avg_duration_minutes: float
    avg_calories_burned: Optional[float] = None
    most_common_workout_type: Optional[str] = None


class WeightStatsOut(BaseModel):
    """Output model for weight statistics."""

    average_weight: float
    weight_change: Optional[float] = None
    weight_change_percentage: Optional[float] = None
    current_weight: Optional[float] = None
    trend: str


@router.get("/stats/workouts", response_model=WorkoutStatsOut, tags=["stats"])
def workout_stats(days: int = 30) -> WorkoutStatsOut:
    """Get workout statistics for the past N days."""

    return WorkoutStatsOut(**ds.get_workout_stats(days=days))


@router.get("/stats/weight", response_model=WeightStatsOut, tags=["stats"])
def weight_stats(days: int = 30) -> WeightStatsOut:
    """Get weight statistics for the past N days."""

    return WeightStatsOut(**ds.get_weight_stats(days=days))


# ------------------------------------------------------------------
# User goals
# ------------------------------------------------------------------


class GoalIn(BaseModel):
    """Input model for fitness goals."""

    goal_type: str = Field(..., min_length=1, example="weight_loss")
    target_weight: Optional[float] = Field(None, gt=0)
    weekly_workouts: int = Field(3, ge=1, le=14)
    daily_calorie_target: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class GoalOut(GoalIn):
    """Output model for fitness goals."""


@router.post("/goals", response_model=GoalOut, status_code=201, tags=["goal"])
def save_goal(body: GoalIn) -> GoalOut:
    """Save user fitness goal."""

    goal = Goal(**body.model_dump())
    ds.save_goal(goal)

    return GoalOut(**body.model_dump())


@router.get("/goals", response_model=GoalOut, tags=["goal"])
def get_goal() -> GoalOut:
    """Get user fitness goal."""

    goal = ds.get_goal()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found",
        )

    return GoalOut(
        goal_type=goal.goal_type,
        target_weight=goal.target_weight_kg,
        weekly_workouts=goal.weekly_workouts,
        daily_calorie_target=goal.daily_calorie_target,
        notes=goal.notes,
    )