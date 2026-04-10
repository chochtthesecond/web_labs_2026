from utils import parse_post_data
import types

def course_list(request, container):
    #GET /courses - список  курсов
    course_repo = container.get('course_repo')
    courses = course_repo.get_all_with_student_count()
    context = {'courses': courses}
    body = container.get('template').render('courses.html', context)
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def course_create_form(request, container):
    #POST /courses/new - форма добавления курса
    context = {
        'form_action': '/courses',
        'method': 'POST',
        'course': None,
        'errors': {}
    }
    body = container.get('template').render('course_form.html', context)
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def course_create(request, container):
    #POST /courses - создание курса
    content_length = request.headers.get('Content-Length')
    if not content_length:
        return ('400 Bad Request', [], 'Missing Content-Length')
    post_data = parse_post_data(content_length, request.rfile)
    title = post_data.get('title', '').strip()
    description = post_data.get('description', '').strip()
    teacher = post_data.get('teacher', '').strip()
    service = container.get('course_service')
    course_id, errors = service.create_course(title, description, teacher)
    if errors:
        #создаем временный курс без id
        course = types.SimpleNamespace(
            id=None,
            title=title,
            description=description,
            teacher=teacher
        )
        context = {
            'form_action': '/courses',
            'method': 'POST',
            'course': course,
            'enrolled_students': [],
            'available_students': [],
            'errors': errors
        }
        body = container.get('template').render('course_form.html', context)
        return ('400 Bad Request', [('Content-Type', 'text/html; charset=utf-8')], body)
    return ('303 See Other', [('Location', '/courses')], '')

def course_edit_form(request, container, course_id):
    #GET courses/<id>/edit - форма редактирования курса
    course_repo = container.get('course_repo')
    service = container.get('course_service')
    course = course_repo.get_by_id(course_id)
    if not course:
        return ('404 Not Found', [('Content-Type', 'text/plain')], 'Course not found')
    enrolled_students = service.get_enrolled_students(course_id)
    available_students = service.get_available_students(course_id)
    context = {
        'form_action': f'/courses/{course_id}/edit',
        'method': 'POST',
        'course': course,
        'enrolled_students': enrolled_students,
        'available_students': available_students,
        'errors': {}
    }
    body = container.get('template').render('course_form.html', context)
    return ('200 OK', [('Content-Type', 'text/html; charset=utf-8')], body)

def course_update(request, container, course_id):
    #POST /courses/<id>/edit - обновление курса
    content_length = request.headers.get('Content-Length')
    if not content_length:
        return ('400 Bad Request', [], 'Missing Content-Length')
    post_data = parse_post_data(content_length, request.rfile)
    title = post_data.get('title', '').strip()
    description = post_data.get('description', '').strip()
    teacher = post_data.get('teacher', '').strip()
    service = container.get('course_service')
    errors = service.update_course(course_id, title, description, teacher)
    if errors:
        course_repo = container.get('course_repo')
        course = course_repo.get_by_id(course_id)
        if not course:
            course = types.SimpleNamespace(
                id=course_id,
                title=title,
                description=description,
                teacher=teacher
            )
        enrolled_students = service.get_enrolled_students(course_id)
        available_students = service.get_available_students(course_id)
        context = {
            'form_action': f'/courses/{course_id}/edit',
            'method': 'POST',
            'course': course,
            'enrolled_students': enrolled_students,
            'available_students': available_students,
            'errors': errors
        }
        body = container.get('template').render('course_form.html', context)
        return ('400 Bad Request', [('Content-Type', 'text/html; charset=utf-8')], body)
    return ('303 See Other', [('Location', f'/courses')], '')

def course_delete(request, container, course_id):
    #POST /courses/<id>/delete - удаление курса
    service = container.get('course_service')
    error = service.delete_course(course_id)
    if error:
        return ('303 See Other', [('Location', f'/courses/{course_id}/edit')], '')
    return ('303 See Other', [('Location', '/courses')], '')

def course_add_student(request, container, course_id):
    #POST /courses/<id>/add_student - запись студента на курс
    content_length = request.headers.get('Content-Length')
    if not content_length:
        return ('400 Bad Request', [], 'Missing Content-Length')
    post_data = parse_post_data(content_length, request.rfile)
    student_id = post_data.get('student_id')
    if not student_id:
        return ('400 Bad Request', [], 'Missing student_id')
    service = container.get('course_service')
    error = service.add_student_to_course(course_id, student_id)
    if error:
        pass
    return ('303 See Other', [('Location', f'/courses/{course_id}/edit')], '')

def course_remove_student(request, container, course_id):
    #POST /courses/<id>/remove_student - отчисление студента с курса
    content_length = request.headers.get('Content-Length')
    if not content_length:
        return ('400 Bad Request', [], 'Missing Content-Length')
    post_data = parse_post_data(content_length, request.rfile)
    student_id = post_data.get('student_id')
    if not student_id:
        return ('400 Bad Request', [], 'Missing student_id')
    service = container.get('course_service')
    error = service.remove_student_from_course(course_id, student_id)
    if error:
        pass
    return ('303 See Other', [('Location', f'/courses/{course_id}/edit')], '')