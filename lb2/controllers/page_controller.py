def index(request, container):
    body = container.get('template').render('index.html')
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def about(request, container):
    body = container.get('template').render('about.html')
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def contact(request, container):
    body = container.get('template').render('contact.html')
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)