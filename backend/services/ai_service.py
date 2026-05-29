"""
AI service integrates with the Mistral API to generate 
personalized fitness and nutrition recommendations.

Requires an environment variable MISTRAL_API_KEY for authentication.
Set with .env file, later via Docker Compose.
"""

import os
from typing import Optional

from mistralai import Mistral

from backend.models import Goal


def _get_client() -> Mistral:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is not set.")
    return Mistral(api_key=api_key)

def _build_context(
        goal: Optional[Goal],
        workout_stats: Optional[dict],
        weight_stats: Optional[dict],
) -> str:
    """Builds a context string for the AI based on user data."""
    lines = ["User fitness data:"]
    if goal:
        lines.append(f"- Goal: {goal.goal_type}")
        if goal.target_weight_kg:
            lines.append(f"- Target weight: {goal.target_weight_kg} kg")
        if goal.weekly_workouts:
            lines.append(f"- Weekly workouts per week: {goal.weekly_workouts}")
        if goal.daily_calorie_target:
            lines.append(f"- Daily calorie target: {goal.daily_calorie_target} kcal")

    if workout_stats and workout_stats.get("total_workouts", 0) > 0:
        lines.append(f"- Workouts last 30 days: {workout_stats['total_workouts']}")
        lines.append(f"- Average duration: {workout_stats['average_duration_minutes']} min")
        lines.append(f"- Total calories burned: {workout_stats['total_calories_burned']} kcal")

    if weight_stats and weight_stats.get("current_weight"):
        lines.append(f"- Current weight: {weight_stats['current_weight']} kg")
        lines.append(f"- Weight trend: {weight_stats['trend']}")
        if weight_stats.get("weight_change_kg"):
            lines.append(f"- Weight change: {weight_stats['weight_change']:+.1f} kg")

    if len(lines) == 1:
        lines.append("- No data available")

    return "\n".join(lines)


def generate_workout_plan(
        goal: Optional[Goal],
        workout_stats: Optional[dict],
        weight_stats: Optional[dict],
) -> str:
    """
    Generate a personalized workout plan based on the user data
    Returns the AI response as a string.
    """
    client = _get_client()
    context = _build_context(goal, workout_stats, weight_stats)

    prompt = f"""You are a professional fitness coach. Based on the following user data, 
create a practical weekly workout plan. Keep it concise and actionable — 
include exercise type, duration, and intensity for each day.
 
{context}
 
Respond in the same language the user's goal is written in. 
Keep the plan realistic and achievable."""
 
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )

    return response.choices[0].message.content


def generate_nutrition_advice(
        goal: Optional[Goal],
        workout_stats: Optional[dict],
        weight_stats: Optional[dict],
) -> str:
    """
    Generate personalised nutrition advice based on user data.
    Returns the AI response as a string.
    """
    client = _get_client()
    context = _build_context(goal, workout_stats, weight_stats)
 
    prompt = f"""You are a certified nutritionist. Based on the following user data,
give practical dietary advice. Include suggested daily calorie intake,
macronutrient split, and 3-4 specific meal ideas.
 
{context}
 
Respond in the same language the user's goal is written in.
Keep the advice evidence-based and practical."""
 
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )

    return response.choices[0].message.content


def generate_motivation(
        goal: Optional[Goal],
        workout_stats: Optional[dict],
        weight_stats: Optional[dict],
) -> str:
    """
    Generate a short motivational message tailored to the user's progress.
    Returns the AI response as a string.
    """
    client = _get_client()
    context = _build_context(goal, workout_stats, weight_stats)
 
    prompt = f"""You are an encouraging fitness coach. Based on the following user data,
write a short (3-4 sentences) personalised motivational message.
Acknowledge their progress and encourage them to keep going.
 
{context}
 
Respond in the same language the user's goal is written in."""
 
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
 
    return response.choices[0].message.content