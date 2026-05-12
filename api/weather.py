import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {
            "temp": 79,
            "feels_like": 76,
            "humidity": 16,
            "wind": "10 mph W",
            "uv": "8 — High",
            "desc": "Sunny",
            "icon": "☀️"
        }
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
