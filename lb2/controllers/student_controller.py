from utils import parse_post_data
import types
    
def student_list(request, container):
    #GET /students - список всех студентов
    student_repo = container.get('student_repo')
    students = student_repo.get_all_as_objects()
    context = {'students': students}
    body = container.get('template').render('students.html', context)
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def student_create_form(request, container):
    #GET /students/new - форма добавления студента
    course_repo = container.get('course_repo')
    courses = course_repo.get_all()
    context = {
        'courses': courses,
        'form_action': '/students',
        'method': 'POST',
        'student': None,
        'errors': {}
    }
    body = container.get('template').render('student_form.html', context)
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def student_create(request, container):
    #POST /students - создание студента
    content_length = request.headers.get('Content-Length')
    if not content_length:
        return ('400 Bad Request', [], 'Missing Content-Length')
    post_data = parse_post_data(content_length, request.rfile)
    name = post_data.get('name', '').strip()
    email = post_data.get('email', '').strip()
    phone = post_data.get('phone', '').strip()

    service = container.get('student_service')
    student_id, errors = service.create_student(name, email, phone)
    if errors:
        course_repo = container.get('course_repo')
        courses = course_repo.get_all()
        context = {'courses': courses,
                   'form_action': '/students',
                   'method': 'POST',
                   'student': types.SimpleNamespace(name=name, email=email, phone=phone),
                   'errors': errors}
        body = container.get('template').render('student_form.html', context)
        return ('400 Bad Request', [('Content-Type', 'text/html; charset=utf-8')], body)
    return ('303 See Other', [('Location', '/students')], '')

def student_edit_form(request, container, student_id):
    #GET /students/<id>/edit - форма редактирования
    student_repo = container.get('student_repo')
    student = student_repo.get_by_id(student_id)
    if not student:
        return ('404 Not Found', [('Content-Type', 'text/plain')], 'Student not found')
    course_repo = container.get('course_repo')
    courses = course_repo.get_all()
    context = {
        'courses': courses,
        'form_action': f'/students/{student_id}/update',
        'method': 'POST',
        'student': student,
        'errors': {}
    }
    body = container.get('template').render('student_form.html', context)
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def student_update(request, container, student_id):
    #POST /students/<id>/update - обновление студента
    content_length = request.headers.get('Content-Length')
    if not content_length:
        return ('400 Bad Request', [], 'Missing Content-Length')
    post_data = parse_post_data(content_length, request.rfile)
    name = post_data.get('name', '').strip()
    email = post_data.get('email', '').strip()
    phone = post_data.get('phone', '').strip()
    service = container.get('student_service')
    errors = service.update_student(student_id, name, email, phone)
    if errors:
        student_repo = container.get('student_repo')
        student = student_repo.get_by_id(student_id)
        course_repo = container.get('course_repo')
        courses = course_repo.get_all()
        context = {'courses': courses,
                   'form_action': f'/students/{student_id}/update',
                   'method': 'POST',
                   'student': types.SimpleNamespace(id=student_id, name=name, email=email, phone=phone),
                   'errors': errors
                   }
        body = container.get('template').render('student_form.html', context)
        return ('400 Bad Request', [('Content-Type', 'text/html; charset=utf-8')], body)
    return ('303 See Other', [('Location', '/students')], '')

def student_delete(request, container, student_id):
    #POST /students/<id>/delete - удаление студента
    service = container.get('student_service')
    error = service.delete_student(student_id)
    if error:
        pass
    return ('303 See Other', [('Location', '/students')], '')