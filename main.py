from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
import sqlite3
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
import hashlib
import random
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


class RightContentCls(IRightBodyTouch, MDBoxLayout):
    icon = StringProperty()
    text = StringProperty()


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


    def menu_callback(self, text_item):
        self.level = f"{text_item}"
        self.root.ids.drop_menu_position.text = f"{text_item}"

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
                generate = random.randint(10000, 100000)
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
