"""
Endpoints for weight.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.models import Weight
from backend.services import data_service as ds

router = APIRouter(prefix="/weight", tags=["weight"])


class WeightIn(BaseModel):
    """Input model for weight entries."""

    date: date
    weight_kg: float = Field(..., gt=0, le=500)


class WeightOut(WeightIn):
    """Output model for weight entries."""

    id: str


@router.post("/", response_model=WeightOut, status_code=201)
def create_weight_entry(body: WeightIn) -> WeightOut:
    """Create a new weight entry."""

    try:
        entry = Weight(**body.model_dump())
        saved = ds.save_weight(entry)

        return WeightOut(
            **body.model_dump(),
            id=saved.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


@router.get("/", response_model=list[WeightOut])
def list_weight_entries(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> list[WeightOut]:
    """List weight entries, optionally filtered by date range."""

    df = ds.get_weight_entries(
        from_date=from_date,
        to_date=to_date,
    )

    if df.empty:
        return []

    return [
        WeightOut(
            date=row["date"],
            weight_kg=row["weight"],
            id=str(row["id"]),
        )
        for _, row in df.iterrows()
    ]