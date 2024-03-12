import pandas as pd
import openpyxl

# Загрузка таблицы Excel
df = pd.read_excel('scr/Книга1.xlsx')

# Изменение формата даты рождения
df['Дата рождения'] = pd.to_datetime(df['Дата рождения']).dt.strftime('%d %m %Y')

# Извлечение даты рождения и ФИО
birthday = df['Дата рождения']
name = df['ФИО']

# Вывод результатов
for i in range(len(birthday)):
    birthday_enter = birthday[i].replace(" ", ".")
    print(f"Дата рождения: {birthday_enter}, ФИО: {name[i]}")