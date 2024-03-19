import sqlite3

with sqlite3.connect('userbase.db') as db:
    cursor = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY,
        id_user TEXT,
        sum INTEGER,
        for_what TEXT,
        time TEXT

    )
    """

    cursor.executescript(query)

    def ebalN():
        values = [51000, -29, "За хорошее поведение", "19:54:13"]
        cursor.execute("INSERT INTO history(id_user, sum, for_what, time) VALUES(?,?,?,?)", values)


    def balance():
        id_user = input("Ведите id_user: ")
        cursor.execute(f'''SELECT * FROM history WHERE id_user LIKE '%{id_user}%';''')
        three_results = cursor.fetchall()
        balance = 0
        for i in range(len(three_results)):
            balance += int(three_results[i][2])
        print(balance)


    action = input("Ведите квпы уца а")
    if action == "Списать":
        ebalN()
    elif action == "Баланс":
        balance()