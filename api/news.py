from flask import Response
import json

def handler(request):
    # TODO: Connect to real news API
    events = [
        {"time": "08:30 ET", "event": "Initial Jobless Claims", "impact": "HIGH"},
        {"time": "10:00 ET", "event": "Existing Home Sales", "impact": "MEDIUM"}
    ]
    return Response(json.dumps(events), mimetype="application/json")