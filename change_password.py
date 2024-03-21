import sqlite3
with sqlite3.connect('userbase.db') as db:
    cursor = db.cursor()
    cursor.execute("UPDATE users SET password = 'Smith' WHERE id_user = 51000")