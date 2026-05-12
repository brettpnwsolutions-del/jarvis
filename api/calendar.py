import json

def handler(request, response):
    data = [
        {"time": "10:00 ET", "summary": "Calendar API not connected", "location": ""}
    ]
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return json.dumps(data)
