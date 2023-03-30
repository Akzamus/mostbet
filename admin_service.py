import sqlite3


class AdminService:
    def __init__(self, db_path):
        self.db_path = db_path

    def add_admin(self, admin_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admins (id) VALUES (?)", admin_id)
            conn.commit()

    def remove_admin(self, admin_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admins WHERE id=?", admin_id)
            conn.commit()

    def is_admin(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM admins WHERE id=?", user_id)
            result = cursor.fetchone()
            return result[0] > 0

    def get_admin_ids(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM admins")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
