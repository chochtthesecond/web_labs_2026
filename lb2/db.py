import psycopg2
import psycopg2.extras
import os

class DatabaseConnection:
    def __init__(self, host, port, user, password, dbname):
        self.params = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'dbname': dbname
        }
        self.connection = None

    def connect(self):
        #устанавливаем соединение с БД, если оно не активно
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(**self.params)
        return self.connection

    def get_cursor(self):
        #возвращает курсор и строки в виде словарей
        conn = self.connect()
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def execute_query(self, sql, params=None, commit=False):
        #выполняет SQL-запрос с параметрами
        cursor = self.get_cursor()
        try:
            cursor.execute(sql,params or ())
            if sql.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                return result
            if commit:
                self.connection.commit()
            return None
        except Exception as e:
            self.connection.rollback() #откатываем изменения
            raise e
        finally:
            cursor.close()