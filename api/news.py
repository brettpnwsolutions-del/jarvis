import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = [
            {"time": "08:30 ET", "event": "Initial Jobless Claims", "impact": "HIGH"},
            {"time": "10:00 ET", "event": "Existing Home Sales", "impact": "MEDIUM"}
        ]
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
