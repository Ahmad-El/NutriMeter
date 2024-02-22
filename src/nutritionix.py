import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

NUT_API_ID = os.getenv("NUT_API_ID")
NUT_API_KEY = os.getenv("NUT_API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
header = {
    "Content-Type": "application/json",
    "x-app-id": NUT_API_ID,
    "x-app-key": NUT_API_KEY,
}

ender = {
    "food": "natural/nutrients",
    "sport": "natural/exercise",
}


def get_responce(type_api: str, query: dict):
    url = f"{ENDPOINT}/{type_api}"
    responce = requests.post(url=url, headers=header, json=query)
    if responce.status_code != 200:
        raise Exception("Connection Error or bad request")
    return responce.json()


def parse_sport(data) -> dict:
    sport = data["exercises"][0]
    return [
        {
            "Sport": sport["name"],
            "Metabolic equivalent of task": sport["met"],
            "Duration": str(sport["duration_min"]) + " min",
            "Calories Expended": str(sport["nf_calories"]) + " kcal",
        }
    ]


def parse_food(data) -> dict:

    return [
        {
            "Food name": food["food_name"],
            "Weight": str(food["serving_weight_grams"]) + "g",
            "Calories": str(food["nf_calories"]) + " kcal",
            "Total Fat": str(food["nf_total_fat"]) + "g",
            "Saturated Fat": str(food["nf_saturated_fat"]) + "g",
            "Cholesterol": str(food["nf_cholesterol"]) + "g",
            "Sodium": str(food["nf_sodium"]) + "g",
            "Total Carbohydrates": str(food["nf_total_carbohydrate"]) + "g",
            "Dietary Fiber": str(food["nf_dietary_fiber"]) + "g",
            "Sugars": str(food["nf_sugars"]) + "g",
            "Protein": str(food["nf_protein"]) + "g",
            "Potassium": str(food["nf_potassium"]) + "g",
        }
        for food in data["foods"]
    ]


if __name__ == "__main__":
    type_api = ender["food"]
    query = {"query": "banana"}
    json_data = get_responce(type_api, query)
    with open("data.json", "w") as file:
        json.dump(json_data, file, indent=4)
    print(parse_food(json_data))
