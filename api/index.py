import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'morning-brief.html')
            with open(template_path, 'r') as f:
                html = f.read()
            body = html.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            body = f'Error: {str(e)}'.encode()
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, format, *args):
        pass
