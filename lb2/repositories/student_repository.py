import types

class StudentRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_all_as_objects(self):
        rows = self.get_all()
        return [types.SimpleNamespace(**dict(row)) for row in rows]
    
    def get_all(self, limit=100, offset=None):
        sql = "SELECT id, name, email, phone, registered_at FROM students ORDER BY id"
        params = []
        if limit is not None:
            sql += " LIMIT %s"
            params.append(limit)
        if offset is not None:
            sql += " OFFSET %s"
            params.append(offset)
        return self.db.execute_query(sql, params)

    def get_by_id(self, student_id):
        sql = "SELECT id, name, email, phone, registered_at FROM students WHERE id = %s"
        result = self.db.execute_query(sql, (student_id,))
        result = result[0] if result else None
        return types.SimpleNamespace(**dict(result)) if result else None

    def create(self, name, email, phone):
        sql = """
            INSERT INTO students (name, email, phone)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        result = self.db.execute_query(sql, (name, email, phone), commit=True)
        return result[0]['id'] if result else None

    def update(self, student_id, name, email, phone):
        sql = """
            UPDATE students
            SET name = %s, email = %s, phone = %s
            WHERE id = %s
        """
        self.db.execute_query(sql, (name, email, phone, student_id), commit=True)

    def delete(self, student_id):
        sql = "DELETE FROM students WHERE id = %s"
        self.db.execute_query(sql, (student_id,), commit=True)

    def is_email_unique(self, email, exclude_id=None):
        """Валидирует уникальность email."""
        sql = "SELECT id FROM students WHERE email = %s"
        if exclude_id:
            sql += " AND id != %s"
            params = (email, exclude_id)
        else:
            params = (email,)
        result = self.db.execute_query(sql, params)
        return len(result) == 0