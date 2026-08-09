import os
import requests
from dotenv import load_dotenv
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(location):
    result = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": location,
            "units": "metric",
            "appid": API_KEY
        }
    )

    data = result.json()

    if data["cod"] == 404:
        return f"I couldn't find the location {location}."

    description = data["weather"][0]["description"]
    temperature = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    high = round(data["main"]["temp_max"])
    low = round(data["main"]["temp_min"])

    location = location.title()

    # Get today's rainfall forecast
    forecast_result = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={
            "q": location,
            "units": "metric",
            "appid": API_KEY
        }
    )

    forecast_data = forecast_result.json()

    today = datetime.now().date()
    rainfall = 0

    for forecast in forecast_data["list"]:
        forecast_time = datetime.fromtimestamp(forecast["dt"])

        if forecast_time.date() == today:
            rainfall += forecast.get("rain", {}).get("3h", 0)

    rainfall = round(rainfall, 1)

    return (
        f"The weather in {location} is {temperature}°C with {description}, "
        f"feels like {feels_like}°C. "
        f"Today's high is {high}°C and today's low is {low}°C. "
        f"About {rainfall} millimetres of rain is expected today."
    )