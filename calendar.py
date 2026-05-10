from flask import Response
import json

def handler(request):
    # TODO: Connect to Google Calendar API
    events = [{"time": "10:00 ET", "summary": "Calendar API not connected", "location": ""}]
    return Response(json.dumps(events), mimetype="application/json")