from dataclasses import dataclass, field
from datetime import date as Date
from typing import Optional

from backend.services.data_service import _generate_id


@dataclass
class Workout:
    id: str = field(default_factory=_generate_id)
    date: Date = None
    type: str = ""
    duration_minutes: int = 0
    calories_burned: Optional[int] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be positive")


@dataclass
class Nutrition:
    id: str = field(default_factory=_generate_id)
    date: Date = None
    meal_name: str = ""
    calories: int = 0
    carbs: Optional[int] = None
    protein: Optional[int] = None
    fat: Optional[int] = None


@dataclass
class Weight:
    id: str = field(default_factory=_generate_id)
    date: Date = None
    weight_kg: float = 0.0


@dataclass
class Goal:
    id: str = field(default_factory=_generate_id)
    goal_type: str = ""
    target_weight_kg: Optional[float] = None
    target_workout_minutes: Optional[int] = None
    target_calories: Optional[int] = None
    notes: Optional[str] = None
    weekly_workouts: int = 0
    daily_calorie_target: Optional[int] = None
