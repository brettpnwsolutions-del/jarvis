import json

def handler(event, context):
    # Placeholder - connect to Google Calendar API for real events
    data = [
        {"time": "10:00 ET", "summary": "Calendar API not connected", "location": ""}
    ]
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(data)
    }