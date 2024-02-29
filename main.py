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
Window.size = (520, 900)

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

    def notification(self):
        self.root.ids.notification_bell.icon = 'bell-ring'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "text": f"Item {i}",
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            header_cls=MenuHeader(),
            caller=self.root.ids.button,
            items=menu_items,
            width_mult=4,
        )

    def menu_callback(self, text_item):
        print(text_item)

    # def on_start(self):
    #     charge_contests = MDDataTable(
    #         column_data=[
    #             ("Уровни", dp(40)),
    #             ("1 место", dp(15)),
    #             ("2 место", dp(15)),
    #             ("3 место", dp(15)),
    #             ("Участие", dp(15)),
    #         ],
    #         row_data=[
    #             (
    #                 "Кванториум_НЧК",
    #                 "3",
    #                 "2",
    #                 "1",
    #                 "-",
    #             ),
    #             (
    #                 "Городской",
    #                 "5",
    #                 "3",
    #                 "2",
    #                 "1",
    #             ),
    #             (
    #                 "Республиканский",
    #                 "7",
    #                 "5",
    #                 "3",
    #                 "2"
    #             ),
    #             (
    #                 "Межрегиональный",
    #                 "10",
    #                 "7",
    #                 "5",
    #                 "3",
    #             ),
    #             (
    #                 "Всероссийский",
    #                 "15",
    #                 "10",
    #                 "7",
    #                 "5",
    #             ),
    #         ],
    #     )
    #     self.root.ids.charge_contests.add_widget(charge_contests)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file("kivy.kv")

    def copy_button_text(self):
        Clipboard.copy(self.root.ids.id_users.text)

    def registration(self):
        login = self.root.ids.log.text
        password = self.root.ids.pase.text
        name = self.root.ids.nameas.text
        age = self.root.ids.age.text
        otch = self.root.ids.otchims.text
        famal = self.root.ids.famalis.text

        fio = f"{age, otch, famal}"
        try:
            db = sqlite3.connect("database.db")
            cursor = db.cursor()

            cursor.execute("SELECT login FROM users WHERE login = ?", [login])

            if cursor.fetchone() is None:
                values = [login, password, fio, age]
                cursor.execute("INSERT INTO users(login, password, name, age) VALUES(?,?,?,?)", values)
                toast("Создали акаунт")
                self.root.ids.screen_manager.current = "Enter"
                db.commit()
            else:
                toast("Tакой логин уже есть")

        except sqlite3.Error as e:
            print("Error", e)
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
                db = sqlite3.connect("database.db")
                cursor = db.cursor()
                cursor.execute("SELECT login FROM users WHERE login = ?", [login])
                if cursor.fetchone() is None:
                    toast("Такого логина не существует")
                else:
                    cursor.execute("SELECT login FROM users WHERE login = ? AND password = md5(?)", [login, password])
                    if cursor.fetchone() is None:
                        toast("Пороль не верный")
                    else:
                        toast("Вы вошли")
                        self.root.ids.screen_manager.current = "search"
            except sqlite3.Error as e:
                print('Error, e')
            finally:
                cursor.close()
                db.close()

    def screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name


MoneyTest().run()
