"""
Simple Fitness Tracker - FastAPI Backend.
Start with `uvicorn main:app --reload` --port 8000.
Swagger UI: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import workouts, nutrition, weight, stats