import sqlite3

with sqlite3.connect('userbase.db') as db:
    cursor = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS history(
        id_user TEXT,
        sum INTEGER,
        for_what TEXT,
        time TEXT

)
    """

    cursor.executescript(query)


def balance_def(id):
    with sqlite3.connect('userbase.db') as db:
        cursor = db.cursor()
        id_user = id.replace("ID:", "")
        cursor.execute(f'''SELECT * FROM history WHERE id_user LIKE '%{id_user}%';''')
        three_results = cursor.fetchall()
        balance = 0
        for i in range(len(three_results)):
            balance += int(three_results[i][1])
    return balance