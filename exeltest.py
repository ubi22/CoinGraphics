import pandas as pd

# Загрузка данных из файла Excel
df = pd.read_excel('scr/Книга1.xlsx')
# Преобразование формата даты
df['Дата рождения'] = pd.to_datetime(df['Дата рождения'], format='%d.%m.%Y').dt.strftime('%d.%m.%Y')

print(df['Дата рождения'])