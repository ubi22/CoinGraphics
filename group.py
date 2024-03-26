import sqlite3
with sqlite3.connect("userbase.db") as db:
    cursor = db.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS groups (
            id_user TEXT,
            name_teacher TEXT,
            id_group TEXT,
            name_group TEXT
        )
        """
    cursor.executescript(query)

    def search():
        group = input("Группа: ")
        db_cursor = db.cursor()
        db_cursor.execute(f'''SELECT * FROM groups WHERE name_group LIKE '%{group}%';''')
        result = db_cursor.fetchall()


    def plus():
        pass

action = input("Введите действие: ")
if action == "Поиск":
    search()
elif action == "Плюс":
    plus()