import types

class CourseRepository:
    def __init__(self, db_connection):
        self.db = db_connection
        
    def get_all_with_student_count(self):
        sql = """
            SELECT c.id, c.title, c.description, c.teacher,
                   COUNT(e.student_id) AS student_count
            FROM courses c
            LEFT JOIN course_enrollments e ON c.id = e.course_id
            GROUP BY c.id
            ORDER BY c.id
        """
        rows = self.db.execute_query(sql)
        return [types.SimpleNamespace(**dict(row)) for row in rows]
        
    def get_all(self):
        sql = "SELECT id, title, description, teacher FROM courses ORDER BY id"
        rows = self.db.execute_query(sql)
        return [types.SimpleNamespace(**dict(row)) for row in rows]
        
    def get_by_id(self, course_id):
        sql = "SELECT id, title, description, teacher FROM courses WHERE id = %s"
        result = self.db.execute_query(sql, (course_id,))
        if not result:
            return None
        return types.SimpleNamespace(**dict(result[0]))
        
    def create(self, title, description, teacher):
        sql = """
            INSERT INTO courses (title, description, teacher)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        result = self.db.execute_query(sql, (title, description, teacher), commit=True)
        return result[0]['id'] if result else None

    def update(self, course_id, title, description, teacher):
        sql = """
            UPDATE courses
            SET title = %s, description = %s, teacher = %s
            WHERE id = %s
        """
        self.db.execute_query(sql, (title, description, teacher, course_id), commit=True)

    def delete(self, course_id):
        sql = "DELETE FROM courses WHERE id = %s"
        self.db.execute_query(sql, (course_id,), commit=True)
        
    def get_enrolled_students(self, course_id):
        sql = """
            SELECT s.id, s.name, s.email
            FROM students s
            JOIN course_enrollments e ON s.id = e.student_id
            WHERE e.course_id = %s
            ORDER BY s.name
        """
        rows = self.db.execute_query(sql, (course_id,))
        return [types.SimpleNamespace(**dict(row)) for row in rows]

    def get_available_students(self, course_id):
        sql = """
            SELECT id, name, email
            FROM students
            WHERE id NOT IN (
                SELECT student_id FROM course_enrollments WHERE course_id = %s
            )
            ORDER BY name
        """
        rows = self.db.execute_query(sql, (course_id,))
        return [types.SimpleNamespace(**dict(row)) for row in rows]

    def add_student_to_course(self, course_id, student_id):
        sql = """
            INSERT INTO course_enrollments (course_id, student_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """
        self.db.execute_query(sql, (course_id, student_id), commit=True)

    def remove_student_from_course(self, course_id, student_id):
        sql = "DELETE FROM course_enrollments WHERE course_id = %s AND student_id = %s"
        self.db.execute_query(sql, (course_id, student_id), commit=True)

    def delete_enrollments_for_course(self, course_id):
        sql = "DELETE FROM course_enrollments WHERE course_id = %s"
        self.db.execute_query(sql, (course_id,), commit=True)