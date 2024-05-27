from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from search import search
from kivymd.uix.list import IconLeftWidget
from kivy.clock import mainthread
import json
import threading
import kvant_lib
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
import hashlib
import random
import requests
from url import url



def get_account(login):
    result = json.loads(requests.get(f"{url}/get_account/{login}").text)
    return result


def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()


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




class SigInt:
    def __init__(self):
        self.val = False

    def set(self, val):
        self.val = val


class MoneyTest(MDApp):
    dialog_report_open = None
    level = ""
    dialog_list = None
    dialog_change = None
    dialog_lan = None
    dialog_confirmation = None
    dialog_settings_account = None
    dialog_confirmation_report = None
    dialog_for_send = None
    name = str
    password = str
    id = str
    dialog_loading = None
    birthday = str
    user_modified = str
    icon = "scr/logo (2).png"
    title = "Kvantomat"
    charge_contests = None
    text_search = ""
    path = ""
    balance = 0
    search_handle: threading.Thread = None
    search_sig_int = SigInt()

    url = "https://kvantomat24.serveo.net"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.fg = None
        self.elevation = 0

    def generate(self):
        while True:
            value = random.randint(10_000, 99_999)
            if not get_account(value):
                return value

    @mainthread
    def send_message(self, message):
        toast(message)

    def create_users_sql(self):
        self.dialog_email_send()

        for i in range(len(self.charge_contests.row_data)):
            if self.charge_contests.row_data[i][3] == "Уже есть":
                self.send_message("Aккаунт создан")
            else:
                json = kvant_lib.create_user(self.charge_contests.row_data[i][0], self.charge_contests.row_data[i][1], self.charge_contests.row_data[i][2], "12345678", self.root.ids.login.text, self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))

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

    def threading_search(self, text):
        if self.search_sig_int.val:
            self.search_sig_int.set(True)
            self.search_handle.join()
            self.search_sig_int.set(False)
            self.clear_list("container")

        self.search_handle = threading.Thread(target=self.search_students,args=(text,))
        self.search_handle.start()

    def search_students(self, text=""):
        my_list = []
        # if len(text) < len(self.text_search):
        #     self.text_search = text
        #     return

        if len(text) >= 4:
            self.clear_list("container")
            search_person = json.loads(requests.get(f"{url}/get_account_skeleton_list").text)
            LIST = search(search_person, text, self.search_sig_int)
            if LIST is None:
                return
            for i in LIST:
                if self.search_sig_int.val:
                    return
                my_list.append(search_person[i])

            self.clear_list("container")
            for i in my_list:
                self.string_person(i)
            self.text_search = text

    @mainthread
    def clear_list(self, id):
        eval(f"self.root.ids.{id}.clear_widgets()")

    @mainthread
    def string_person(self, puple):
        self.root.ids.container.add_widget(
            ThreeLineIconListItem(
                text=puple['name'],
                secondary_text=puple['birthdate'],
                tertiary_text=f"ID: {puple['id']}",
                on_release=lambda x: self.dialog_windows(x)
            ),
        )

    def balance_def(self, ids):
        id_user = ids.replace("ID: ", "")
        balance = json.loads(requests.get(f"{url}/get_account/{id_user}").text)["balance"]
        self.dialog_list.text = f'Баланс: {balance}'
        return balance

    def dialog_windows(self, task_windows):
        print(task_windows.text, task_windows.secondary_text)
        self.name = task_windows.text
        self.birthday = task_windows.secondary_text
        self.id = task_windows.tertiary_text
        threading.Thread(target=self.balance_def, args=(self.id,)).start()
        if self.dialog_list:
            self.dialog_list = None
        if not self.dialog_list:
            self.dialog_list = MDDialog(
                title=f"{self.name}",
                text=f"Баланс: Загрузка...",
                type="simple",
                radius=[20, 7, 20, 7],
                items=[
                    Item(text="Удалить", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Сбросить пароль", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Начислить", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                    Item(text="Списание", on_release=lambda x=task_windows.text: self.dialog_windows_task(x)),
                ],

            )
            self.dialog_list.open()
    @mainthread
    def dialog_close(self, a):
        eval(f"self.{a}.dismiss()")

    @mainthread
    def dialog_email_send(self):
        if not self.dialog_for_send:
            self.dialog_for_send = MDDialog(
                radius=[20, 7, 20, 7],
                title="Введите почту для отправки копии списков",
                type="custom",
                auto_dismiss=False,
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

    def dialog_windows_change(self):
        self.dialog_close("dialog_list")
        if self.dialog_change:
            self.dialog_change = None
        if not self.dialog_change:
            self.dialog_change = MDDialog(
                radius=[20, 7, 20, 7],
                title=f"",
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
                        on_release=lambda x: self.threading("settings_balance")
                    ),
                ],

            )
            self.dialog_change.open()

    def dialog_windows_confirmation(self):
        if not self.dialog_confirmation:
            self.dialog_confirmation = MDDialog(
                title=f"Вы точно хотите удалить: \n{self.name}",
                text="Все данные о пользователе будут стерты безвозратно",
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
                        on_release=lambda x: self.threading("clear_account")
                    ),
                ],
            )
        self.dialog_confirmation.open()

    def clear_account(self):
        id = self.id.replace("ID: ", "")
        self.dialog_close("dialog_confirmation")
        self.dialog_close("dialog_list")
        if self.dialog_confirmation.text == "Все данные о пользователе будут стерты безвозратно":
            json = kvant_lib.delete_user(id, self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            self.send_message("Аккаунт удален")
        else:
            json = kvant_lib.change_password(id, "12345678",self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            self.send_message("Пароль сброшен")
        self.threading_action("self.root.ids.container.clear_widgets()")

    @mainthread
    def threading_action(self, action):
        eval(action)

    def dialog_windows_task(self, task):
        task = task.text
        if task == "Сбросить пароль":
            self.dialog_windows_confirmation()
            self.dialog_confirmation.text = "Пароль будет по умолчанию: 12345678"
            self.dialog_confirmation.title = f"Вы точно хотите сбросить пароль: \n{self.name}?"
        elif task == "Удалить":
            self.dialog_windows_confirmation()
            self.dialog_confirmation.text = f"Все данные о пользователе будут стерты безвозратно"
            self.dialog_confirmation.title = f"Вы точно хотите удалить: \n{self.name}?"
        elif task == "Начислить":
            self.dialog_windows_change()
            self.dialog_change.title = "Начислить"
            self.dialog_change.content_cls.ids.first_field.hint_text = "Сколько"
            self.dialog_change.content_cls.ids.secondary_field.hint_text = "За что"
        elif task == "Списание":
            self.dialog_windows_change()
            self.dialog_change.title = "Списать"
            self.dialog_change.content_cls.ids.first_field.hint_text = "Сколько"
            self.dialog_change.content_cls.ids.secondary_field.hint_text = "За что"

    def menu_callback(self, text_item):
        self.level = f"{text_item}"
        self.root.ids.drop_menu_position.text = f"{text_item}"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_file("kivy.kv")

    def settings_balance(self):
        try:
            sum = int(self.dialog_change.content_cls.ids.first_field.text)
            if len(self.dialog_change.content_cls.ids.secondary_field.text) < 8:
                self.send_message("Введите за что")
                return
            balance = self.balance_def(self.id)
            print(self.id)
            id = self.id.replace("ID: ", "")
            print(self.dialog_change.title)
            if self.dialog_change.title == "Списать":
                if balance < sum:
                    self.send_message("Недостаточно средст")
                else:
                    json = kvant_lib.change_balance(-sum, id, self.dialog_change.content_cls.ids.secondary_field.text, self.root.ids.login.text, self.root.ids.password.text)
                    requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
                    self.send_message("Списано")
                    self.dialog_close("dialog_change")
            elif self.dialog_change.title == "Начислить":
                json = kvant_lib.change_balance(sum, id, self.dialog_change.content_cls.ids.secondary_field.text, self.root.ids.login.text, self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
                self.send_message("Начислино")
                self.dialog_close("dialog_change")
        except ValueError:
            self.send_message("Введите сумму начисления")

    def threading(self, fun):
        eval(f"threading.Thread(target=self.{fun}).start()")

    def dialog_report(self):
        if not self.dialog_report_open:
            self.dialog_report_open = MDDialog(
                radius=[20, 7, 20, 7],
                title="Куда отправить",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="email_field",
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
                        on_release=lambda x: self.send_report()
                    ),
                ],

            )
        self.dialog_report_open.open()

    def update(self):
        login = self.root.ids.login.text
        account = get_account(login)
        history = account["history"]
        self.root.ids.scroll_history.clear_widgets()
        for i in reversed(history):
            self.root.ids.scroll_history.add_widget(
                ThreeLineIconListItem(
                    IconLeftWidget(
                        icon="history"
                    ),
                    text=str(i['sum']),
                    secondary_text=f"{i['for_what']}",
                    tertiary_text=str(i['time'])
                )
            )
        self.root.ids.balance_user.text = f"{self.balance_def(login)} Kvant"

    def registration(self):
        login = self.root.ids.login_admin_new.text
        password = self.root.ids.password_admin_new.text
        name = self.root.ids.name_admin_new.text
        birthday = self.root.ids.birthday_admin_new.text
        email = self.root.ids.email_new_admin.text

        for i in (login, password, name, birthday, email):
            if not len(i):
                toast("Вы заполнили не все поля")

                return

        if get_account(login):
            toast("Такой логин есть")
        else:
            print("My login is:")
            print(self.root.ids.login.text)
            json = kvant_lib.create_user(login, name, birthday, password, self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            self.screen("admin_screen")
            toast("Создали аккаунт")

    def dialog_settings_accounts(self):
        if not self.dialog_settings_account:
            self.dialog_settings_account = MDDialog(
                title="Измените пароль по умолчанию",
                type="custom",
                auto_dismiss=False,
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
        pass

    def settings_password(self):
        requests.get(f"{url}/passwd?login={self.root.ids.login.text}&new_password={hashlib.sha256(self.dialog_settings_account.content_cls.ids.password_input.text.encode()).hexdigest()}")
        self.dialog_close("dialog_settings_account")

    def log_in(self):
        try:
            login = self.root.ids.login.text
            password = self.root.ids.password.text
            self.root.ids.spinner_login_screen.active = True
            check = requests.get(f"{url}/check_login_credentials?login={login}&password={hashlib.sha256(password.encode()).hexdigest()}").text
            print(f"The check is: {check}")
            check = json.loads(check)
            if check:
                account = get_account(login)
                self.login_interface(login, password, account)

            else:
                self.send_message("Введены неверные данные")
                self.root.ids.spinner_login_screen.active = False
        except json.decoder.JSONDecodeError:
        # except TypeError:
            self.send_message("Ошибка сервера")
            self.root.ids.spinner_login_screen.active = False

    @mainthread
    def login_interface(self, login, password, account):
        id_ = account["id"]
        fullname = account["name"]
        balance = account["balance"]
        history = account["history"]
        birthdate = account["birthdate"]

        name = dict(enumerate(fullname.split(" "))).get(1) or fullname
        family = dict(enumerate(fullname.split(" "))).get(0) or fullname
        dad = dict(enumerate(fullname.split(" "))).get(2) or fullname
        toast("Вы вошли")

        if len(login) == 5:
            self.id = login
            self.password = password
            self.root.ids.screen_manager.current = "main_screen"
            print(history)
            self.root.ids.balance_user.text = f"{balance} Kvant"
            self.root.ids.name_profile_main.text = f"{family} {name} \n{dad}"
            self.root.ids.name_main_screen.text = f"{name} >"
        elif len(login) == 6:
            self.root.ids.screen_manager.current = "teacher_screen"
            self.root.ids.name_teacher_screen.text = name
            self.root.ids.id_teacher_screen.text = id_
            self.root.ids.birthday_teacher_screen.text = birthdate
        elif len(login) == 7:
            self.root.ids.screen_manager.current = "teacher_screen"
            self.root.ids.admin_name.text = account["name"]
            self.root.ids.name_teacher_screen.text = "Администрация"
            self.root.ids.birthday_teacher_screen.text = "26.11.1991"
            self.root.ids.id_teacher_screen.text = 'admin'
        if password == "12345678":
            self.dialog_settings_accounts()
        self.root.ids.spinner_login_screen.active = False

    def screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name

    def confirmation_report(self):
        if not self.dialog_confirmation_report:
            self.dialog_confirmation_report = MDDialog(
                title=f"Вы точно хотите cбросить полугодие?",
                text="Полугодие будет закрыто и отчет начнется заново",
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close("dialog_confirmation_report")
                    ),
                    MDFlatButton(
                        text="Да",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.threading("reset_rating")
                    ),
                ],
            )
        self.dialog_confirmation_report.open()

    def reset_rating(self):
        json = kvant_lib.reset_raiting(self.root.ids.login.text, self.root.ids.password.text)
        requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
        self.dialog_close("dialog_confirmation_report")
        print("Конец")

if __name__ == "__main__":
    MoneyTest().run()
