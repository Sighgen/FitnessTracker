"""Data models for workout, nutrition, weight, and goal tracking."""

from dataclasses import dataclass, field
from datetime import date as Date
from typing import Optional

from backend.services.data_service import _generate_id


# =====================================================
# WORKOUT
# =====================================================

@dataclass
class Workout:
    """Represents a workout session."""

    id: str = field(default_factory=_generate_id)
    date: Date = field(default_factory=Date.today)
    type: str = ""
    duration_minutes: int = 0
    calories_burned: Optional[int] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be a positive integer.")

        if self.calories_burned is not None and self.calories_burned < 0:
            raise ValueError("Calories burned must be non-negative.")


# =====================================================
# NUTRITION
# =====================================================

@dataclass
class Nutrition:
    """Represents nutritional information for a meal."""

    id: str = field(default_factory=_generate_id)
    date: Date = field(default_factory=Date.today)
    meal_name: str = ""
    calories: int = 0
    carbs: Optional[int] = None
    protein: Optional[int] = None
    fat: Optional[int] = None

    def __post_init__(self) -> None:
        if self.calories < 0:
            raise ValueError("Calories must be non-negative.")

        for name in ("carbs", "protein", "fat"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be non-negative.")


# =====================================================
# WEIGHT
# =====================================================

@dataclass
class Weight:
    """Represents a weight entry."""

    id: str = field(default_factory=_generate_id)
    date: Date = field(default_factory=Date.today)
    weight_kg: float = 0.0

    def __post_init__(self) -> None:
        if self.weight_kg <= 0:
            raise ValueError("Weight must be a positive number.")


# =====================================================
# GOAL
# =====================================================

@dataclass
class Goal:
    """Represents a user fitness goal."""

    id: str = field(default_factory=_generate_id)
    goal_type: str = ""

    target_weight_kg: Optional[float] = None
    target_workout_minutes: Optional[int] = None
    target_calories: Optional[int] = None
    notes: Optional[str] = None

    weekly_workouts: int = 0
    daily_calorie_target: Optional[int] = None