import re

class CourseService:
    def __init__(self, course_repo, logger):
        self.repo = course_repo
        self.logger = logger

    def validate_course(self, title):
        errors = {}
        if not title or len(title) > 100:
            errors['title'] = 'Название обязательно и не должно превышать 100 символов'
        return errors

    def create_course(self, title, description, teacher):
        errors = self.validate_course(title)
        if errors:
            return None, errors
        try:
            course_id = self.repo.create(title, description, teacher)
            self.logger.info(f"Создан курс id={course_id} {title}")
            return course_id, None
        except Exception as e:
            self.logger.error(f"Ошибка создания курса: {e}")
            return None, {'db': 'Ошибка базы данных'}

    def update_course(self, course_id, title, description, teacher):
        errors = self.validate_course(title)
        if errors:
            return errors
        try:
            self.repo.update(course_id, title, description, teacher)
            self.logger.info(f"Обновлён курс id={course_id}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка обновления курса: {e}")
            return {'db': 'Ошибка базы данных'}

    def delete_course(self, course_id):
        try:
            self.repo.delete(course_id)
            self.logger.info(f"Удалён курс id={course_id}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка удаления курса: {e}")
            return {'db': 'Ошибка базы данных'}
     
    def get_enrolled_students(self, course_id):
        return self.repo.get_enrolled_students(course_id)

    def get_available_students(self, course_id):
        return self.repo.get_available_students(course_id)

    def add_student_to_course(self, course_id, student_id):
        try:
            self.repo.add_student_to_course(course_id, student_id)
            self.logger.info(f"Студент {student_id} записан на курс {course_id}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка добавления студента на курс: {e}")
            return {'db': 'Не удалось записать студента'}

    def remove_student_from_course(self, course_id, student_id):
        try:
            self.repo.remove_student_from_course(course_id, student_id)
            self.logger.info(f"Студент {student_id} отчислен с курса {course_id}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка удаления студента с курса: {e}")
            return {'db': 'Не удалось отчислить студента'}