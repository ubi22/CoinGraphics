import sqlite3


def balance_def(id):
    with sqlite3.connect('userbase.db') as db:
        cursor = db.cursor()
        id_user = id.replace("ID:", "")
        cursor.execute(f'''SELECT * FROM history WHERE id_user LIKE '%{id_user}%';''')
        three_results = cursor.fetchall()
        balance = 0
        for i in range(len(three_results)):
            balance += int(three_results[i][2])
    return balance