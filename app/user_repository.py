from app.database import get_connection
from app.models import User

class UserRepository:
    def add(self, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            register = cursor.lastrowid
            return register
        
    def get_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            users = [User(id=row[0], name=row[1]) for row in users]
            return users
        
    def get_by_id(self, user_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            if user:
                return User(id=user[0], name=user[1])
            return None