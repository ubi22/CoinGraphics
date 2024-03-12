from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
import pandas as pd
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import ThreeLineIconListItem
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
import sqlite3
from kivy.metrics import dp
from kivymd.uix.list import IconRightWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
import hashlib
import random
import os
Window.size = (520, 900)


def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()


with sqlite3.connect('userbase.db') as db:
    cursor = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        id_user TEXT,
        password TEXT,
        name TEXT,
        birthday TEXT

)
    """

    cursor.executescript(query)


class Content(BoxLayout):
    pass


class Item(OneLineAvatarIconListItem):
    left_icon = StringProperty()
    right_icon = StringProperty()
    right_text = StringProperty()


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MenuHeader(MDBoxLayout):
    '''An instance of the class that will be added to the menu header.'''


class MoneyTest(MDApp):
    level = ""
    dialog_list = None
    dialog_change = None
    dialog_confirmation = None
    name = str
    id = int
    birthday = str
    user_modified = str
    icon = "scr/logo (2).png"
    title = "Kvantomat"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )
        self.file_manager.ext = [".xlsx"]

    def manager_file_exel_open(self):
        self.manager_open = True
        self.file_manager.show(os.path.expanduser("/"))

    def select_path(self, path):
        self.exit_manager()
        toast(f"{path}")

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def notification(self):
        self.root.ids.notification_bell.icon = 'bell-ring'

    def on_start(self):
        charge_contests = MDDataTable(
            column_data=[
                ("Уровни", dp(40)),
                ("1 место", dp(15)),
                ("2 место", dp(15)),
                ("3 место", dp(15)),
                ("Участие", dp(15)),
            ],
            row_data=[
                (
                    "Кванториум_НЧК",
                    "3",
                    "2",
                    "1",
                    "-",
                ),
                (
                    "Городской",
                    "5",
                    "3",
                    "2",
                    "1",
                ),
                (
                    "Республиканский",
                    "7",
                    "5",
                    "3",
                    "2"
                ),
                (
                    "Межрегиональный",
                    "10",
                    "7",
                    "5",
                    "3",
                ),
                (
                    "Всероссийский",
                    "15",
                    "10",
                    "7",
                    "5",
                ),
            ],
        )
        self.root.ids.charge_contests.add_widget(charge_contests)

    def search_students(self, text="", search=False):
        if len(text) >= 4:
            with sqlite3.connect('userbase.db') as db:
                cursor = db.cursor()
                cursor.execute(f'''SELECT * FROM users WHERE name LIKE '%{text}%';''')
                three_results = cursor.fetchall()
                print(three_results)
                self.root.ids.container.clear_widgets()
                for i in range(len(three_results)):
                    self.root.ids.container.add_widget(
                        ThreeLineIconListItem(
                            text=f'{three_results[i][3]}',
                            secondary_text=f"{three_results[i][4]}",
                            tertiary_text=f"ID: {three_results[i][1]}",
                            on_press=lambda x: self.dialog_windows(x)
                        ),
                    )

    def dialog_windows(self, task_windows):
        self.name = task_windows.text
        self.birthday = task_windows.secondary_text
        self.id = task_windows.tertiary_text
        if not self.dialog_list:
            self.dialog_list = MDDialog(
                title=f"{task_windows.text}",
                type="simple",
                radius=[20, 7, 20, 7],
                items=[
                    Item(text="Сбросить пароль", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Удалить", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Начислить", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Списание", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                ],

            )
        self.dialog_list.open()

    def dialog_close(self, a):
        print(a)
        eval(f"self.{a}.dismiss()")

    def dialog_windows_change(self, task_name):
        self.dialog_close("dialog_list")
        if not self.dialog_change:
            self.dialog_change = MDDialog(
                radius=[20, 7, 20, 7],
                title=f"{task_name}",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="first_field",
                        hint_text=f"Пороль",
                    ),
                    MDTextField(
                        id="secondary_field",
                        hint_text=f"Потвердите пороль",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close("dialog_change")
                    ),
                    MDFlatButton(
                        text="Отредактировать",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ],

            )
        self.dialog_change.open()

    def dialog_windows_confirmation(self):
        if not self.dialog_confirmation:
            self.dialog_confirmation = MDDialog(
                title=f"Вы точно хотите удалить: \n{self.name}",
                text="Все данные о пользователе будут стерты без возратно",
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close("dialog_confirmation")
                    ),
                    MDFlatButton(
                        text="Да",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_change_end(x)
                    ),
                ],
            )
        self.dialog_confirmation.open()

    def dialog_change_end(self, task):
        with sqlite3.connect('userbase.db') as db:
            cursor = db.cursor()
            task = task.text
            if task == "Изменить пароль":
                cursor.execute("")
            elif task == "Удалить":
                pass
            elif task == "Начислить":
                pass
            elif task == "Списание":
                pass

    def dialog_windows_task(self, task):
        task = task.text
        if task == "Сбросить пароль":
            self.dialog_windows_confirmation()
            self.dialog_confirmation.text = "Пароль будет по умолчанию: 12345678"
            self.dialog_confirmation.title = f"Вы точно хотите сбросить пароль: \n{self.name}?"
        elif task == "Удалить":
            self.dialog_windows_confirmation()
            self.dialog_confirmation.text = f"Все данные о пользователе будут стерты без возратно"
            self.dialog_confirmation.title = f"Вы точно хотите удалить: \n{self.name}?"
        elif task == "Начислить":
            self.dialog_windows_change(task)
            self.dialog_change.title = "Начислить"
            self.dialog_change.content_cls.ids.first_field.hint_text = "Сколько"
            self.dialog_change.content_cls.ids.secondary_field.hint_text = "За что"
        elif task == "Списание":
            self.dialog_windows_change(task)
            self.dialog_change.title = "Списать"
            self.dialog_change.content_cls.ids.first_field.hint_text = "Сколько"
            self.dialog_change.content_cls.ids.secondary_field.hint_text = "За что"

    def menu_callback(self, text_item):
        self.level = f"{text_item}"
        self.root.ids.drop_menu_position.text = f"{text_item}"

    def excel_enter(self):
        df = pd.read_excel('scr/Книга1.xlsx')
        df['Дата рождения'] = pd.to_datetime(df['Дата рождения']).dt.strftime('%d %m %Y')
        birthday = df['Дата рождения']
        name = df['ФИО']
        for i in range(len(birthday)):
            birthday_enter = birthday[i].replace(" ", ".")
            print(f"Дата рождения: {birthday_enter}, ФИО: {name[i]}")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file("kivy.kv")

    def copy_button_text(self):
        Clipboard.copy(self.root.ids.id_users.text)

    def generate(self):
        with sqlite3.connect('userbase.db') as db:
            cursor = db.cursor()
            while True:
                generate = random.randint(100000, 1000000)
                print(generate)
                cursor.execute("SELECT id_user FROM users WHERE id_user = ?", [generate])
                if cursor.fetchone() is None:
                    self.root.ids.login_admin_new.text = f"{generate}"
                    break

    def registration(self, how_screen):
        if how_screen == "Admin_screen":
            login = self.root.ids.login_admin_new.text
            password = self.root.ids.password_admin_new.text
            name = self.root.ids.name_admin_new.text
            birthday = self.root.ids.birthday_admin_new.text
        else:
            pass

        try:
            db = sqlite3.connect("userbase.db")
            cursor = db.cursor()
            db.create_function("md5", 1, md5sum)
            cursor.execute("SELECT id_user FROM users WHERE id_user = ?", [login])

            if cursor.fetchone() is None:
                values = [login, password, name, birthday]
                cursor.execute("INSERT INTO users(id_user, password, name, birthday) VALUES(?,md5(?),?,?)", values)
                toast("Создали акаунт")
                self.screen("login_screen")
                # self.root.ids.screen_manager.current = "Enter"
                db.commit()
            else:
                toast("Tакой логин уже есть")

        finally:
            cursor.close()
            db.close()

    def log_in(self):
        login = self.root.ids.login.text
        password = self.root.ids.password.text
        if login == 'admin':
            if password == '1234':
                toast("Здраствуйте Admin")
                self.root.ids.screen_manager.current = "admin_screen"
        else:
            try:
                db = sqlite3.connect("userbase.db")
                cursor = db.cursor()
                db.create_function("md5", 1, md5sum)
                cursor.execute("SELECT id_user FROM users WHERE id_user = ?", [login])
                if cursor.fetchone() is None:
                    toast("Такого логина не существует")
                else:
                    cursor.execute("SELECT id_user FROM users WHERE id_user = ? AND password = md5(?)", [login, password])
                    if cursor.fetchone() is None:
                        toast("Пороль не верный")
                    else:
                        if len(login) == 5:
                            toast("Вы вошли")
                            cursor.execute(f'''SELECT * FROM users WHERE id_user LIKE '%{login}%';''')
                            three_results = cursor.fetchall()
                            name = three_results[0][3]
                            name = name.split()
                            birthday = three_results[0][4]
                            self.root.ids.name_main_screen.text = f"{name[1]} >"
                            self.root.ids.name_profile_main.text = f"{name[0]}\n {name[1]} {name[2]}"
                            self.root.ids.birthday_profile_main.text = f"{birthday}"
                            self.root.ids.screen_manager.current = "main_screen"
                        elif len(login) == 6:
                            toast("Вы вошли")
                            self.root.ids.screen_manager.current = "teacher_screen"
                        elif len(login) == 7:
                            toast("Вы вошли")
                            self.root.ids.screen_manager.current = "admin_screen"

            finally:
                cursor.close()
                db.close()

    def screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name


MoneyTest().run()
