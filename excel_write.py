import pandas as pd
import openpyxl
import random


def generate_excel(excel_file):
    df = pd.read_excel("D:\Книга1.xlsx")
    df['Дата рождения'] = pd.to_datetime(df['Дата рождения']).dt.strftime('%d %m %Y')
    birthday = df['Дата рождения']
    name = df['ФИО']
    parents_name = df['Родители']
    parents_email = df['Почта']
    phone = df['Контакты']
    enter_list = []

    class LIST:
        def __init__(self):
            self.birthday = []
            self.name_students = []
            self.name_parents = []
            self.phone_number = []
            self.email_parents = []

    list = LIST()
    for i in range(len(birthday)):
        list.birthday.append(birthday[i])
        list.name_students.append(name[i])
        list.name_parents.append(parents_name[i])
        list.phone_number.append(phone[i])
        list.email_parents.append(parents_email[i])
    enter_list.append(["ФИО", list.name_students])
    enter_list.append(["Дата рождения", list.birthday])
    enter_list.append(["Родители", list.name_parents])
    enter_list.append(["Телефон", list.phone_number])
    enter_list.append(["Почта", list.email_parents])
    enter_list = dict(enter_list)
    df = pd.DataFrame(enter_list)
    df.to_excel('./list_user.xlsx')

generate_excel("adad")