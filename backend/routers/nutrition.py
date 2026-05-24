"""
Endpoints for nutrition.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


from backend.models import Nutrition
from backend.services import data_service as ds

router = APIRouter(prefix="/nutrition", tags=["nutrition"])


class NutritionIn(BaseModel):
    """Input model for nutrition entries."""

    date: date
    meal_name: str = Field(..., min_length=1, example="Breakfast")
    calories: int = Field(..., ge=0)
    carbs: Optional[int] = Field(None, ge=0)
    protein: Optional[int] = Field(None, ge=0)
    fat: Optional[int] = Field(None, ge=0)


class NutritionOut(NutritionIn):
    """Output model for nutrition entries."""

    id: str


class DailyCaloriesOut(BaseModel):
    """Output model for daily calories summary."""

    date: date
    total_calories: int


@router.post("/", response_model=NutritionOut, status_code=201)
def create_nutrition_entry(nutrition: NutritionIn) -> NutritionOut:
    """Create a new nutrition entry."""

    try:
        entry = Nutrition(**nutrition.model_dump())
        saved = ds.save_nutrition(entry)

        return NutritionOut(
            **nutrition.model_dump(),
            id=saved.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get("/", response_model=list[NutritionOut])
def list_nutrition_entries(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> list[NutritionOut]:
    """List nutrition entries, optionally filtered by date range."""

    df = ds.get_nutrition(
        from_date=from_date,
        to_date=to_date,
    )

    if df.empty:
        return []

    def _safe_float(value: object) -> Optional[float]:
        try:
            parsed = float(value)
            return parsed if parsed >= 0 else None
        except (TypeError, ValueError):
            return None

    return [
        NutritionOut(
            id=row["id"],
            date=row["date"],
            meal_name=row["meal_name"],
            calories=row["calories"],
            carbs=_safe_float(row["carbs"]),
            protein=_safe_float(row["protein"]),
            fat=_safe_float(row["fat"]),
        )
        for _, row in df.iterrows()
    ]


@router.get("/daily/{target_date}", response_model=DailyCaloriesOut)
def get_daily_calories(target_date: date) -> DailyCaloriesOut:
    """Get total calories for a specific date."""

    total = ds.get_daily_calories(target_date)

    return DailyCaloriesOut(
        date=target_date,
        total_calories=total,
    )