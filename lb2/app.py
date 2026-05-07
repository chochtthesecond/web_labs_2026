import os
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from config import load_env
from container import build_container
from schema import ensure_schema

class RequestHandler(BaseHTTPRequestHandler):
    container = None #будет установлен в main

    def do_GET(self):
        self._handle_request('GET')

    def do_POST(self):
        self._handle_request('POST')

    def _handle_request(self, method):
        #маршруты: (method,path_pattern)->(controller)
        routes = [
            ('GET', r'^/$', 'index'),
            ('GET', r'^/about$', 'about'),
            ('GET', r'^/contact$', 'contact'),
            ('GET', r'^/students$', 'student_list'),
            ('GET', r'^/students/new$', 'student_create_form'),
            ('POST', r'^/students$', 'student_create'),
            ('GET', r'^/students/(\d+)/edit$', 'student_edit_form'),
            ('POST', r'^/students/(\d+)/update$', 'student_update'),
            ('POST', r'^/students/(\d+)/delete$', 'student_delete'),
            ('GET', r'^/courses$', 'course_list'),
            ('GET', r'^/courses/new$', 'course_create_form'),
            ('POST', r'^/courses$', 'course_create'),
            ('GET', r'^/courses/(\d+)/edit$', 'course_edit_form'),
            ('POST', r'^/courses/(\d+)/edit$', 'course_update'),
            ('POST', r'^/courses/(\d+)/delete$', 'course_delete'),
            ('POST', r'^/courses/(\d+)/add_student$', 'course_add_student'),
            ('POST', r'^/courses/(\d+)/remove_student$', 'course_remove_student')
        ]
        print(self.path)
        for route_method, pattern, controller_name in routes:
            if method != route_method:
                continue
            match = re.match(pattern, self.path)
            if match:
                #извлекаем id, если есть
                args = match.groups()
                #получаем функцию контроллера
                controller = self._get_controller(controller_name)
                if controller:
                    status, headers, content = controller(self, self.container, *args)
                    self.send_response(int(status.split()[0]))
                    for key, val in headers:
                        self.send_header(key, val)
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                    return
        #статические файлы
        if self.path.startswith('/static/'):
            self._serve_static()
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'404 Not Found')

    def _get_controller(self, name):
        #возвращает контроллер
        from controllers.page_controller import index, about, contact
        from controllers.student_controller import (
            student_list, student_create_form, student_create,
            student_edit_form, student_update, student_delete
        )
        from controllers.course_controller import (
            course_list, course_create_form, course_create,
            course_edit_form, course_update, course_delete,
            course_add_student, course_remove_student
        )
        controllers = {
            'index': index,
            'about': about,
            'contact': contact,
            'student_list': student_list,
            'student_create_form': student_create_form,
            'student_create': student_create,
            'student_edit_form': student_edit_form,
            'student_update': student_update,
            'student_delete': student_delete,
            'course_list': course_list,
            'course_create_form': course_create_form,
            'course_create': course_create,
            'course_edit_form': course_edit_form,
            'course_update': course_update,
            'course_delete': course_delete,
            'course_add_student': course_add_student,
            'course_remove_student': course_remove_student
        }
        return controllers.get(name)

    def _serve_static(self):
        #возвращает статические файлы (css,js,img)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        #находим папку со статикой
        static_dir = os.path.join(base_dir, 'static')
        path = self.path[1:]  #убираем первый /
        #преобразуем в абсолютный путь и проверяем, что он внутри static_dir
        full_path = os.path.abspath(os.path.join(static_dir, os.path.relpath(path, 'static')))
        if not full_path.startswith(static_dir) or not os.path.exists(full_path) or not os.path.exists(path) or os.path.isdir(path):
            self.send_response(404)
            self.end_headers()
            return
        with open(path, 'rb') as f:
            content = f.read()
            
        self.send_response(200)
        if path.endswith('.css'):
            self.send_header('Content-Type', 'text/css')
        elif path.endswith('.js'):
            self.send_header('Content-Type', 'application/javascript')
        elif path.endswith('.png'):
            self.send_header('Content-Type', 'image/png')
        elif path.endswith('.jpg') or path.endswith('.jpeg'):
            self.send_header('Content-Type', 'image/jpeg')
        else:
            self.send_header('Content-Type', 'application/octet-stream')
        self.end_headers()
        self.wfile.write(content)

def main():
    load_env()
    container = build_container()
    db = container.get('db')
    logger = container.get('logger')
    ensure_schema(db, logger)
    
    RequestHandler.container = container

    #открываем сервер
    host = '0.0.0.0'
    port = 8080
    server = HTTPServer((host, port), RequestHandler)
    logger.info(f'Сервер запущен на http://{host}:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('Остановка сервера')
        server.shutdown()

if __name__ == '__main__':
    main()