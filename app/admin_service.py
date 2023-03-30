from typing import List
import sqlite3


class AdminService:
    def __init__(self, db_path: str, main_admin_id: int):
        self.__db_path: str = db_path
        self.__main_admin_id: int = main_admin_id
        self.create_admins_table()

    def add_admin(self, admin_id: int) -> None:
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admins (id) VALUES (?)", (admin_id,))
            conn.commit()

    def remove_admin(self, admin_id: int) -> None:
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admins WHERE id=?", (admin_id,))
            conn.commit()

    def is_admin(self, user_id: int) -> bool:
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM admins WHERE id=?", (user_id,))
            result = cursor.fetchone()
            return result[0] > 0

    def get_admin_ids(self) -> List[int]:
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM admins")
            rows = cursor.fetchall()
            return [row[0] for row in rows]

    def create_admins_table(self):
        with sqlite3.connect(self.__db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS admins
                         (id INTEGER PRIMARY KEY)''')

    def get_main_admin_id(self) -> int:
        return self.__main_admin_id
