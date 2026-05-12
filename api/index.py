import os

def handler(request, response):
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'morning-brief.html')
    with open(template_path, 'r') as f:
        html = f.read()
    response.status_code = 200
    response.headers['Content-Type'] = 'text/html'
    return html
