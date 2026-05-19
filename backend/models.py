from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Workout:
    id: int
    date: date
    type: str
    duration_minutes: int
    calories_burned: Optional[int] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if self.duration_minutes <= 0:
            raise ValueError("Duration must be a positive integer.")

        if self.calories_burned is not None and self.calories_burned < 0:
            raise ValueError("Calories burned must be a non-negative integer.")


@dataclass
class Nutrition:
    date: date
    meal_name: str
    calories: int
    carbs: Optional[int] = None
    protein: Optional[int] = None
    fat: Optional[int] = None

    def __post_init__(self) -> None:
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
    date: date
    weight_kg: float

    def __post_init__(self) -> None:
        if self.weight_kg <= 0:
            raise ValueError("Weight must be a positive number.")


@dataclass
class Goal:
    goal_type: str
    target_weight_kg: Optional[float] = None
    target_workout_minutes: Optional[int] = None
    target_calories: Optional[int] = None
    notes: Optional[str] = None