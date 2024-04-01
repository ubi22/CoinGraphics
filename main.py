from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
import random
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivy import platform
import os

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
    dialog_settings_account = None
    dialog_for_send = None
    name = str
    id = int
    birthday = str
    icon = "scr/logo (2).png"
    title = "Kvantomat"
    user_modified = str
    charge_contests = None
    path = None
    balance = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )
        self.file_manager.ext = [".xlsx"]
        self.fg = None
        self.elevation = 0

    def manager_file_exel_open(self):
        PATH = "."
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            app_folder = os.path.dirname(os.path.abspath(__file__))
            PATH = "/storage/emulated/0"  # app_folder
        self.file_manager.show(PATH)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        self.root.ids.generate_table.clear_widgets()
        self.path = path
        try:
            self.root.ids.boxlayout_download.pos_hint = ({"center_x": .3, "center_y": .1})
            self.fg = MDRaisedButton(
                    id="rr",
                    text='Создать пользователей',
                    pos_hint=({"center_x": .7, "center_y": .1}),
                    on_release=lambda x: self.create_users_sql()

                )
            self.root.ids.boxlayout.add_widget(self.fg)

        except(KeyError):
            toast("Неправильные столбцы")

    def create_users_sql(self):
        toast("Создан")
        self.dialog_email_send()

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
        self.root.ids.text_hint_create.text = """Для создания пользователе\n1: Выберети файл формата Excel\n2: Проверьте данные сгенерировав таблицу\n4: Создайте пользователей\n3: Отправте на почту копию таблицы        """
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

    def send_mail(self):
        if len(self.dialog_for_send.content_cls.ids.email_for_send.text) == 0:
            toast("Введите почту")
        else:
            self.screen("teacher_screen")
            self.dialog_close("dialog_for_send")

    def search_students(self, text="", search=False):
        self.root.ids.container.clear_widgets()
        for i in range(2):
            self.root.ids.container.add_widget(
                ThreeLineIconListItem(
                    text=f'Васильев Андрей Витальевич',
                    secondary_text=f"02.10.2009",
                    tertiary_text=f"ID: 265265",
                    on_release=lambda x: self.dialog_windows(x)
                ),
            )

    def dialog_windows(self, task_windows):
        print(task_windows.text, task_windows.secondary_text)
        self.name = task_windows.text
        self.birthday = task_windows.secondary_text
        self.id = task_windows.tertiary_text
        if self.dialog_list:
            self.dialog_list = None
        if not self.dialog_list:
            self.dialog_list = MDDialog(
                title=f"Васильев Андрей Витальевич",
                text=f"Баланс: 25",
                type="simple",
                radius=[20, 7, 20, 7],
                items=[
                    Item(text="Сбросить пароль", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Начислить", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Списание", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                ],

            )
            self.dialog_list.open()

    def dialog_close(self, a):
        print(a)
        eval(f"self.{a}.dismiss()")

    def dialog_email_send(self):
        if not self.dialog_for_send:
            self.dialog_for_send = MDDialog(
                radius=[20, 7, 20, 7],
                title="Введите почту для отправки копии списков",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="email_for_send",
                        hint_text="Почта",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="60dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="Отправить",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.send_mail()
                    ),
                ],

            )
        self.dialog_for_send.open()

    def dialog_windows_change(self, task_name):
        self.dialog_close("dialog_list")
        if self.dialog_change:
            self.dialog_change = None
        if not self.dialog_change:
            self.dialog_change = MDDialog(
                radius=[20, 7, 20, 7],
                title=f"{task_name}",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="first_field",
                        input_filter='float',
                        hint_text=f"Пароль",
                    ),
                    MDTextField(
                        id="secondary_field",
                        hint_text=f"Потвердите пароль",
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
                        on_release=lambda x: self.settings_balance(task_name)
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
                        on_release=lambda x: self.clear_account()
                    ),
                ],
            )
        self.dialog_confirmation.open()

    def clear_account(self):
        if self.dialog_confirmation.text == "Все данные о пользователе будут стерты без возратно":
            toast("Аккаунт удален")
            self.dialog_close("dialog_confirmation")
            self.dialog_close("dialog_list")
        else:
            toast("Пароль сброшен")
            self.dialog_close("dialog_confirmation")
            self.dialog_close("dialog_list")
            self.root.ids.container.clear_widgets()

    def generate(self):
        a = random.randint(10000, 99999)
        self.root.ids.login_admin_new.text = f"{a}"

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

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_file("kivy.kv")

    def settings_balance(self, confirm):
        if confirm == "Списание":
            toast("Списано")
            self.dialog_close("dialog_change")
        elif confirm == "Начислить":
            toast("Начислино")
            self.dialog_close("dialog_change")

    def registration(self, how_screen):

        if how_screen == "Admin_screen":
            login = self.root.ids.login_admin_new.text
            password = self.root.ids.password_admin_new.text
            name = self.root.ids.name_admin_new.text
            birthday = self.root.ids.birthday_admin_new.text
            email = self.root.ids.email_new_admin.text

        toast("Создали аккаунт")
        self.screen("login_screen")

    def dialog_settings_accounts(self):
        if not self.dialog_settings_account:
            self.dialog_settings_account = MDDialog(
                title="Измените пароль по умолчанию",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="password_input",
                        hint_text=f"Пароль",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="60dp",
                ),
                buttons=[
                    MDRaisedButton(
                        text="Изменить",
                        on_release=lambda x: self.settings_password()
                    ),
                ],
            )
        self.dialog_settings_account.open()

    def user_scroll_balance(self, ids):
        for i in range(2):
            self.root.ids.scroll_history.add_widget(
                ThreeLineIconListItem(
                    IconLeftWidget(
                        icon="history"
                    ),
                    text=f"15",
                    secondary_text=f"За хорошое поведение",
                    tertiary_text=f"02.09.2023"
                ))

    def settings_password(self):
        toast("Изменить пароль")
        self.dialog_close("dialog_settings_account")

    def log_in(self):
        login = self.root.ids.login.text
        password = self.root.ids.password.text
        if login == 'admin':
            if password == '1234':
                toast("Здраствуйте Admin")
                self.root.ids.screen_manager.current = "admin_screen"
        else:
            if len(login) == 5:
                toast("Вы вошли")
                self.root.ids.screen_manager.current = "main_screen"
                if password == "12345678":
                    self.dialog_settings_accounts()
            elif len(login) == 6:
                toast("Вы вошли")
                self.root.ids.screen_manager.current = "teacher_screen"
            elif len(login) == 7:
                toast("Вы вошли")
                self.root.ids.screen_manager.current = "admin_screen"

    def screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name


MoneyTest().run()
