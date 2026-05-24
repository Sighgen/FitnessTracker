"""
Simple Fitness Tracker - FastAPI Backend.
Start with `uvicorn main:app --reload` --port 8000.
Swagger UI: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import workouts, nutrition, weight, stats

app = FastAPI(title="Simple Fitness Tracker",
                description="A simple fitness tracking API built with FastAPI.",
                version="1.0.0"
)


# Allow Streamlit (port 8501) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workouts.router)
app.include_router(nutrition.router)
app.include_router(weight.router)
app.include_router(stats.router)


@app.get("/", tags=["status"])
def root() -> dict:
    return {"status": "OK", "message": "Welcome to the Simple Fitness Tracker API!"}

