"""
AI endpoints generates workout plans, nutrition advice, and motivation
with Mistral from user stored data.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services import ai_service, data_service as ds

router = APIRouter(prefix="/ai", tags=["AI"])

class AIResponse(BaseModel):
    """Response model for AI-generated content.
    """
    response: str


def _load_context() -> dict:
    """Load user data to pass as context for AI"""
    return {
        "goal": ds.get_goal(),
        "workout_stats": ds.get_workout_stats(days=30),
        "weight_stats": ds.get_weight_stats(days=30),
    }

@router.get("/workout-plan", response_model=AIResponse)
def get_workout_plan() -> AIResponse:
    """Generate personalized workout plan based on user data."""
    try:
        ctx = _load_context()
        result = ai_service.generate_workout_plan(**ctx)
        return AIResponse(response=result)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {e}")
    

@router.get("/nutrition-advice", response_model=AIResponse)
def get_nutrition_advice() -> AIResponse:
    """Generate personalized nutrition advice based on user data."""
    try:
        ctx = _load_context()
        result = ai_service.generate_nutrition_advice(**ctx)
        return AIResponse(response=result)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {e}")
    

@router.get("/motivation", response_model=AIResponse)
def get_motivation() -> AIResponse:
    """Generate personalized motivation based on user data."""
    try:
        ctx = _load_context()
        result = ai_service.generate_motivation(**ctx)
        return AIResponse(response=result)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {e}")