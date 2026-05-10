import os
from flask import Response, send_from_directory

def handler(request):
    try:
        with open('templates/morning-brief.html', 'r') as f:
            html = f.read()
        return Response(html, mimetype='text/html')
    except Exception as e:
        return Response('Error: ' + str(e), mimetype='text/html', status=500)
