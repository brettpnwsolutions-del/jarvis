import json

def handler(request):
    path = request.path
    
    if path == '/' or path == '' or path == '/morning-brief.html':
        try:
            with open('templates/morning-brief.html', 'r') as f:
                html = f.read()
            from flask import Response
            return Response(html, mimetype='text/html')
        except Exception as e:
            from flask import Response
            return Response('Error: ' + str(e), mimetype='text/html', status=500)
    
    elif path == '/api/market':
        from flask import Response
        return Response(json.dumps({'status': 'ok', 'message': 'market api working'}), mimetype='application/json')
    
    elif path == '/api/weather':
        from flask import Response
        return Response(json.dumps({'temp': 79, 'desc': 'Sunny'}), mimetype='application/json')
    
    from flask import Response
    return Response('Not Found', mimetype='text/plain', status=404)

app = handler
