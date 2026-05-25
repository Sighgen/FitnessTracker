"""
Endpoints for stats.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.models import Goal
from backend.services import data_service as ds

router = APIRouter(tags=["stats"])


# =====================================================
# STATS MODELS
# =====================================================


class WorkoutStatsOut(BaseModel):
    """Output model for workout statistics."""

    total_workouts: int
    total_duration: int
    total_calories: int
    average_duration: int
    average_calories: int


class WeightStatsOut(BaseModel):
    """Output model for weight statistics."""

    current_weight: Optional[float]
    average_weight: float
    weight_change: Optional[float]
    weight_change_percentage: Optional[float]
    trend: str


# =====================================================
# STATS ROUTES
# =====================================================


@router.get("/stats/workouts", response_model=WorkoutStatsOut)
def workout_stats(days: int = 30) -> WorkoutStatsOut:
    """Get workout statistics for the past N days."""
    return WorkoutStatsOut(**ds.get_workout_stats(days=days))


@router.get("/stats/weight", response_model=WeightStatsOut)
def weight_stats(days: int = 30) -> WeightStatsOut:
    """Get weight statistics for the past N days."""
    return WeightStatsOut(**ds.get_weight_stats(days=days))


# =====================================================
# GOALS
# =====================================================


class GoalIn(BaseModel):
    """Input model for fitness goals."""

    goal_type: str = Field(..., min_length=1)
    target_weight_kg: Optional[float] = Field(None, gt=0)
    weekly_workouts: int = Field(3, ge=1, le=14)
    daily_calorie_target: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class GoalOut(GoalIn):
    """Output model for fitness goals."""

    id: Optional[str] = None


# -----------------------------------------------------
# Save goal
# -----------------------------------------------------


@router.post("/goals", response_model=GoalOut, status_code=201)
def save_goal(body: GoalIn) -> GoalOut:
    """Save user fitness goal."""

    goal = Goal(**body.model_dump())
    saved = ds.save_goal(goal)

    return GoalOut(**body.model_dump(), id=saved.id)


# -----------------------------------------------------
# Get goal
# -----------------------------------------------------


@router.get("/goals", response_model=GoalOut)
def get_goal() -> GoalOut:
    """Get user fitness goal."""

    goal = ds.get_goal()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found",
        )

    return GoalOut(
        id=goal.id,
        goal_type=goal.goal_type,
        target_weight_kg=goal.target_weight_kg,
        weekly_workouts=goal.weekly_workouts,
        daily_calorie_target=goal.daily_calorie_target,
        notes=goal.notes,
    )