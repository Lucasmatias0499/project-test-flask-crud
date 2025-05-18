from app.database import get_connection


class UserRepository:
    def add(self, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            register = cursor.lastrowid
            return register