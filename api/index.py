from flask import Response

def handler(request):
    return Response('Hello from Jarvis!', mimetype='text/plain')

app = handler
