import json

def handler(request, response):
    data = [
        {"time": "08:30 ET", "event": "Initial Jobless Claims", "impact": "HIGH"},
        {"time": "10:00 ET", "event": "Existing Home Sales", "impact": "MEDIUM"}
    ]
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(data)
