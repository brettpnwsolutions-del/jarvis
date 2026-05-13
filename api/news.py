import json

def handler(event, context):
    # Placeholder economic news
    data = [
        {"time": "08:30 ET", "event": "Initial Jobless Claims", "impact": "HIGH"},
        {"time": "10:00 ET", "event": "Existing Home Sales", "impact": "MEDIUM"}
    ]
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(data)
    }