import os
from password import password
import smtplib
from tkinter import filedialog
import tkinter as tk
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from kivymd.toast import toast
import mimetypes
from email import encoders


def send_em(sub:str = 'Списки учеников', message:str = 'Здесь вы можете увидеть список учеников и посмотреть их пароли и логины', res_mail: str = 'ms447404@mail.ru'):
    global password
    sender = 'nchk-kvantomat@yandex.ru'
    passwor = password

    try:
        with open('list_user.xlsx', 'rb') as file_x:
            ftype, enocodin = mimetypes.guess_type(file_x.name)
            print(ftype)
            file_type, sub_type = ftype.split('/')
            file = MIMEBase(file_type, sub_type)
            file.set_payload(file_x.read())
            encoders.encode_base64(file)

    except IOError:
        return f"No found {file_x.name}"

    file.add_header('content-disposition', 'attachment', filename=file_x.name)
    #msg = MIMEText(f'{message}', 'plain', 'utf-8')
    msg = MIMEMultipart()
    msg.attach(file)
    #msg = MIMEText(template, 'html')
    msg.attach(MIMEText(f'{message}', 'plain','utf-8'))
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = sender
    msg['To'] = res_mail

    try:
        server = smtplib.SMTP('smtp.ya.ru', 587, timeout=15)
        server.starttls()
        server.login(sender, passwor)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        return toast('Отправленно')

    except ValueError as e:
        return toast(f'Ошибка: -> {e}')

    finally:
        server.quit()
