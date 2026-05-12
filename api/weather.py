import json

def handler(request, response):
    data = {
        "temp": 79,
        "feels_like": 76,
        "humidity": 16,
        "wind": "10 mph W",
        "uv": "8 — High",
        "desc": "Sunny",
        "icon": "☀️"
    }
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(data)
