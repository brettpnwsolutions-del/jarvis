import json
import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Using Open-Meteo free API (no key needed)
            lat = 39.5296
            lon = -119.8138
            
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
            
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            code = current.get("weather_code", 0)
            weather_map = {
                0: ("☀️", "Clear"), 1: ("🌤", "Mainly Clear"), 2: ("⛅", "Partly Cloudy"),
                3: ("☁️", "Overcast"), 45: ("🌫", "Fog"), 48: ("🌫", "Fog"),
                51: ("🌧", "Drizzle"), 53: ("🌧", "Drizzle"), 55: ("🌧", "Drizzle"),
                61: ("🌧", "Rain"), 63: ("🌧", "Rain"), 65: ("🌧", "Rain"),
                71: ("🌨", "Snow"), 73: ("🌨", "Snow"), 75: ("🌨", "Snow"),
                80: ("🌦", "Rain Showers"), 81: ("🌦", "Rain Showers"), 82: ("🌦", "Rain Showers"),
                95: ("⛈", "Thunderstorm"), 96: ("⛈", "Thunderstorm"), 99: ("⛈", "Thunderstorm"),
            }
            icon, desc = weather_map.get(code, ("☀️", "Clear"))
            
            result = {
                "temp": round(current.get("temperature_2m", 0)),
                "feels_like": round(current.get("apparent_temperature", 0)),
                "humidity": round(current.get("relative_humidity_2m", 0)),
                "wind": f"{round(current.get('wind_speed_10m', 0))} mph",
                "uv": str(round(current.get("uv_index", 0))),
                "desc": desc,
                "icon": icon,
                "high": round(daily.get("temperature_2m_max", [0])[0], 1) if daily.get("temperature_2m_max") else "--",
                "low": round(daily.get("temperature_2m_min", [0])[0], 1) if daily.get("temperature_2m_min") else "--"
            }
            
            body = json.dumps(result).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)
            
        except Exception as e:
            fallback = {"temp": 72, "feels_like": 70, "humidity": 45, "wind": "5 mph", "uv": "5", "desc": "Sunny", "icon": "☀️", "high": 78, "low": 55}
            body = json.dumps(fallback).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, format, *args):
        pass