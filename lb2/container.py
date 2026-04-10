import os
from logger import Logger
from db import DatabaseConnection
from repositories.student_repository import StudentRepository
from repositories.course_repository import CourseRepository
from services.student_service import StudentService
from services.course_service import CourseService
from render import Template

class Container:
    def __init__(self):
        self._factories = {}
        self._instances = {}

    def register(self, name, factory):
        self._factories[name] = factory

    def get(self, name):
        if name not in self._instances:
            factory = self._factories.get(name)
            if not factory:
                raise KeyError(f"Service '{name}' not registered")
            self._instances[name] = factory()
        return self._instances[name]

#инициализация контейнера
def build_container():
    container = Container()

    #регистрируем логгер
    container.register('logger', lambda: Logger())

    #регистрируем подключение к БД через .env
    def build_db():
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        user = os.getenv('DB_USER', 'music_user')
        password = os.getenv('DB_PASSWORD', 'securepass')
        dbname = os.getenv('DB_NAME', 'music_school')
        return DatabaseConnection(host, port, user, password, dbname)
    container.register('db', build_db)

    #регистрируем репозитории
    def build_student_repo():
        return StudentRepository(container.get('db'))
    container.register('student_repo', build_student_repo)

    def build_course_repo():
        return CourseRepository(container.get('db'))
    container.register('course_repo', build_course_repo)

    #регистрируем сервисы
    def build_student_service():
        return StudentService(container.get('student_repo'), container.get('logger'))
    container.register('student_service', build_student_service)
    
    def build_course_service():
        return CourseService(container.get('course_repo'), container.get('logger'))
    container.register('course_service', build_course_service)
    
    #регистрируем шаблон страниц
    def build_template():
        return Template(template_dir='templates')
    container.register('template', build_template)
    
    return container