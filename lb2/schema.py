import logging

CREATE_TABLES_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS courses (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        teacher VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS course_enrollments (
        student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
        course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (student_id, course_id)
    )
    """
]

def ensure_schema(db_connection, logger=None):
    #создает таблицы, если их нет
    try:
        for statement in CREATE_TABLES_STATEMENTS:
            db_connection.execute_query(statement, commit=True)
        if logger:
            logger.info("Tables created (if missing).")
    except Exception as e:
        if logger:
            logger.error(f"Schema creation failed: {e}")
        raise