from mistralai import Mistral
import os
from backend.services import data_service as ds


class AIService:
    def __init__(self):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    def generate_coaching_response(self):
        # 1. Get from system
        workout_stats = ds.get_workout_stats(30)
        nutrition_stats = ds.get_nutrition_stats(30)
        weight_stats = ds.get_weight_stats(30)
        goal = ds.get_goal()

        # 2. Build prompt
        prompt = f"""
You are a fitness coach. Analyze the user's recent fitness data and provide insights and recommendations.

User's data (last 30 days):

WORKOUTS:
{workout_stats}

NUTRITION:
{nutrition_stats}

WEIGHT:
{weight_stats}

GOALS:
{goal}

Give:
1. Analyses of the user's situation
2. 3 concrete improvements
3. A short training recommendation for next week
4. A diet recommendation
"""

        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content