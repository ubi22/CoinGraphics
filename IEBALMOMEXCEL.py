import pandas as pd
import openpyxl
import random

df = pd.read_excel('scr/Книга1.xlsx')
df['Дата рождения'] = pd.to_datetime(df['Дата рождения']).dt.strftime('%d %m %Y')
birthday = df['Дата рождения']
name = df['ФИО']
parents_name = df['Родители']
parents_email = df['Почта']
phone = df['Контакты']
class LIST:
    def __init__(self):
        self.birthday = []
        self.name_students = []
        self.name_parents = []
        self.phone_number = []
        self.email_parents = []
list = LIST()
list.name_parents
for i in range(len(birthday)):
    birthday = birthday[i].replace(" ", ".")
    list.birthday.append(birthday)
    list.name_students.append(name[i])
    list.name_students.append([i])
