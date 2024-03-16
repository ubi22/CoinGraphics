import pandas as pd
import openpyxl
import random
import sqlite3


df = pd.read_excel('scr/Книга1.xlsx')
enter_birthday = []
enter_name = []
print(enter_birthday)
df['Дата рождения'] = pd.to_datetime(df['Дата рождения']).dt.strftime('%d %m %Y')
birthday = df['Дата рождения']
name = df['ФИО']
parents_name = df['Родители']
parents_email = df['Почта']
phone = df['Контакты']
name_n = []
birthday_n = []
generate_list = []
email_list = []
phone_list = []
parents_name_list = []

with sqlite3.connect('userbase.db') as db:
    cursor = db.cursor()
    def generate():
        while True:
            generate = random.randint(10000, 100000)
            cursor.execute("SELECT id_user FROM users WHERE id_user = ?", [generate])
            if cursor.fetchone() is None:
                break
        return generate

    for i in range(len(birthday)):
        if type(parents_email[i]) == float:
            parents_email = "Отсутсвует"
        elif type(phone[i]) == float:
            phone = "Отсутсвует"
        birthday_enter = birthday[i].replace(" ", ".")
        parents = parents_email[i].split(",")
        print(parents[0])
        cursor.execute(f'''SELECT * FROM users WHERE name LIKE '%{name[i]}%';''')
        three_results = cursor.fetchall()
        if len(three_results) > 0:
            generates = three_results[0][1]
            birthday_n.append(f"{birthday_enter}")

            name_n.append(f"{name[i]}")
            generate_list.append(f'{generates}')
        else:
            generates = generate()
            birthday_n.append(f"{birthday_enter}")
            name_n.append(f"{name[i]}")
            generate_list.append(f'{generates}')

    enter_birthday.append(["День рождение", birthday_n])
    enter_birthday.append(["ФИО", name_n])
    enter_birthday.append(["Логин", generate_list])
    enter_birthday.append(["Пороль", "12345678"])
    users_list = dict(enter_birthday)
    print(users_list)
    df = pd.DataFrame(users_list)
    df.to_excel('./list_user.xlsx')