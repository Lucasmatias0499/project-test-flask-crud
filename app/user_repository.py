from app.database import get_connection
from app.models import User

class UserRepository:    
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
        
    def add(self, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
            conn.commit()
            register = cursor.lastrowid
            return register
        
    def update(self, user_id, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
            conn.commit()
        return self.get_by_id(user_id)
    
    def delete(self, user_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
                