from flask import Response, jsonify

def handler(request):
    return Response("<h1>J.A.R.V.I.S.</h1><p>Go to <a href='/morning-brief.html'>/morning-brief.html</a></p>", mimetype="text/html")