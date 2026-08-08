import requests

api_key = "af9f513c4bd4addd322c7d4cc869732d"

while True:
    location = input("Location: ")

    result = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": location,
            "units": "metric",
            "appid": api_key
        }
    )

    data = result.json()

    print(data)

    if data["cod"] == "404":
        print("Invalid location!")
        continue

    break

description = data["weather"][0]["description"]
temperature = round(data["main"]["temp"])
feels_like = round(data["main"]["feels_like"])
high = round(data["main"]["temp_max"])
low = round(data["main"]["temp_min"])

location = location.title()

print(f"The weather in {location} is {temperature}°C with {description}.")
print(f"It feels like {feels_like}°C.")
print(f"Today's high is {high}°C and today's low is {low}°C.")