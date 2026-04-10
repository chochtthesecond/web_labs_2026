import re

class StudentService:
    def __init__(self, student_repo, logger):
        self.repo = student_repo
        self.logger = logger

    def validate_student(self, name, email, phone, exclude_id=None):
        errors = {}
        if not name or len(name) > 100:
            errors['name'] = 'Имя обязательно и не должно превышать 100 символов'
        if not email:
            errors['email'] = 'Email обязателен'
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors['email'] = 'Некорректный формат email'
        elif not self.repo.is_email_unique(email, exclude_id):
            errors['email'] = 'Этот email уже используется'
        if phone and not re.match(r'^\+?[0-9\s\-\(\)]{10,20}$', phone):
            errors['phone'] = 'Некорректный номер телефона'
        return errors

    def create_student(self, name, email, phone):
        errors = self.validate_student(name, email, phone)
        if errors:
            return None, errors
        try:
            student_id = self.repo.create(name, email, phone)
            self.logger.info(f"Создан студент id={student_id} {name}")
            return student_id, None
        except Exception as e:
            self.logger.error(f"Ошибка создания студента: {e}")
            return None, {'db': 'Ошибка базы данных'}

    def update_student(self, student_id, name, email, phone):
        errors = self.validate_student(name, email, phone, exclude_id=student_id)
        if errors:
            return errors
        try:
            self.repo.update(student_id, name, email, phone)
            self.logger.info(f"Обновлён студент id={student_id}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка обновления студента: {e}")
            return {'db': 'Ошибка базы данных'}

    def delete_student(self, student_id):
        try:
            self.repo.delete(student_id)
            self.logger.info(f"Удалён студент id={student_id}")
            return None
        except Exception as e:
            self.logger.error(f"Ошибка удаления студента: {e}")
            return {'db': 'Ошибка базы данных'}