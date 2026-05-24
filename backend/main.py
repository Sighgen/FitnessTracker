"""
Simple Fitness Tracker - FastAPI Backend.

Start with:
    uvicorn main:app --reload --port 8000

Swagger UI:
    http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import nutrition, stats, weight, workouts

app = FastAPI(
    title="Simple Fitness Tracker",
    description="A simple fitness tracking API built with FastAPI.",
    version="1.0.0",
)

# -------------------------------------------------
# CORS (for Streamlit + frontend access)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Routers
# -------------------------------------------------
app.include_router(workouts.router)
app.include_router(nutrition.router)
app.include_router(weight.router)
app.include_router(stats.router)


# -------------------------------------------------
# Health check
# -------------------------------------------------
@app.get("/", tags=["status"])
def root() -> dict[str, str]:
    """Root endpoint / health check."""

    return {
        "status": "ok",
        "message": "Simple Fitness Tracker API is running",
    }


@app.get("/health", tags=["status"])
def health() -> dict[str, str]:
    """Simple health check endpoint."""

    return {"status": "ok"}
