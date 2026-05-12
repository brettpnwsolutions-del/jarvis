import json
import urllib.request
from http.server import BaseHTTPRequestHandler

# Brett's location - Spokane, WA
LAT = 47.6588
LON = -117.4260

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={LAT}&longitude={LON}"
                f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
                f"wind_speed_10m,weather_code,uv_index"
                f"&daily=temperature_2m_max,temperature_2m_min"
                f"&temperature_unit=fahrenheit&wind_speed_unit=mph"
                f"&timezone=America/Los_Angeles&forecast_days=1"
            )
            with urllib.request.urlopen(url) as res:
                raw = json.loads(res.read())

            current = raw["current"]
            daily = raw["daily"]

            # Map weather code to description and icon
            code = current["weather_code"]
            if code == 0:
                desc, icon = "Clear Sky", "☀️"
            elif code in [1, 2]:
                desc, icon = "Partly Cloudy", "⛅"
            elif code == 3:
                desc, icon = "Overcast", "☁️"
            elif code in [51, 53, 55, 61, 63, 65]:
                desc, icon = "Rainy", "🌧️"
            elif code in [71, 73, 75, 77]:
                desc, icon = "Snowy", "❄️"
            elif code in [80, 81, 82]:
                desc, icon = "Showers", "🌦️"
            elif code in [95, 96, 99]:
                desc, icon = "Thunderstorm", "⛈️"
            else:
                desc, icon = "Cloudy", "☁️"

            data = {
                "temp": round(current["temperature_2m"]),
                "feels_like": round(current["apparent_temperature"]),
                "humidity": round(current["relative_humidity_2m"]),
                "wind": f"{round(current['wind_speed_10m'])} mph",
                "uv": str(round(current.get("uv_index", 0))),
                "desc": desc,
                "icon": icon,
                "high": round(daily["temperature_2m_max"][0]),
                "low": round(daily["temperature_2m_min"][0])
            }

        except Exception as e:
            data = {
                "temp": "--", "feels_like": "--", "humidity": "--",
                "wind": "--", "uv": "--", "desc": "Unavailable",
                "icon": "❓", "high": "--", "low": "--",
                "error": str(e)
            }

        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
