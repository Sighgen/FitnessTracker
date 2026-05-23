"""Data models for workout, nutrition, weight, and goal tracking."""

from dataclasses import dataclass
from datetime import date as Date
from typing import Optional


@dataclass
class Workout:
    """Represents a workout session."""

    id: int
    date: Date
    type: str
    duration_minutes: int
    calories_burned: Optional[int] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate workout values."""
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be a positive integer.")

        if self.calories_burned is not None and self.calories_burned < 0:
            raise ValueError("Calories burned must be a non-negative integer.")


@dataclass
class Nutrition:
    """Represents nutritional information for a meal."""

    date: Date
    meal_name: str
    calories: int
    carbs: Optional[int] = None
    protein: Optional[int] = None
    fat: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate nutrition values."""
        if self.calories < 0:
            raise ValueError("Calories must be a non-negative integer.")

        if self.carbs is not None and self.carbs < 0:
            raise ValueError("Carbs must be a non-negative integer.")

        if self.protein is not None and self.protein < 0:
            raise ValueError("Protein must be a non-negative integer.")

        if self.fat is not None and self.fat < 0:
            raise ValueError("Fat must be a non-negative integer.")


@dataclass
class Weight:
    """Represents a weight entry."""

    date: Date
    weight_kg: float

    def __post_init__(self) -> None:
        """Validate weight value."""
        if self.weight_kg <= 0:
            raise ValueError("Weight must be a positive number.")


@dataclass
class Goal:
    """Represents a user fitness goal."""

    goal_type: str
    target_weight_kg: Optional[float] = None
    target_workout_minutes: Optional[int] = None
    target_calories: Optional[int] = None
    notes: Optional[str] = None