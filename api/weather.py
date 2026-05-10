from flask import Response
import json
import random

def handler(request):
    weather_data = {
        "temp": random.randint(65, 85),
        "feels_like": random.randint(60, 80),
        "humidity": random.randint(20, 60),
        "wind": f"{random.randint(5, 20)} mph NW",
        "uv": f"{random.randint(1, 10)}",
        "desc": random.choice(["Sunny", "Partly Cloudy", "Clear"]),
        "icon": random.choice(["☀️", "⛅", "🌤️"])
    }
    return Response(json.dumps(weather_data), mimetype="application/json")