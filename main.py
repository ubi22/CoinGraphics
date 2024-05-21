from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from search import search
from kivymd.uix.list import IconLeftWidget
from balance import balance_def
import random
from kivy.clock import mainthread
import json
import time
import threading
import kvant_lib
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
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
import hashlib
import platform
import time
import random
import os, pandas, requests
from url import url
Window.size = (520, 900)


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
    birthday = str
    user_modified = str
    icon = "scr/logo (2).png"
    title = "Kvantomat"
    charge_contests = None
    path = ""
    balance = 0

    url = "https://kvantomat24.serveo.net"

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
        self.fg = None
        self.elevation = 0

    def manager_file_exel_open(self):
        PATH = "/"
        self.file_manager.show(PATH)  # output manager to the screen
        self.manager_open = True

    def generate(self):
        while True:
            value = random.randint(10_000, 99_999)
            if not get_account(value):
                return value

    def select_path(self, path):
        self.exit_manager()
        self.root.ids.generate_table.clear_widgets()
        print(path)
        self.path = path
        threading.Thread(target=self.excel_read).start()

    def excel_read(self):
        try:
            print(self.path)
            df = pandas.read_excel(f'{self.path}')
            df['Дата рождения'] = pandas.to_datetime(df['Дата рождения']).dt.strftime('%d %m %Y')
            birthday = df['Дата рождения']
            name = df['ФИО']
            name_parents = df["Родители"]
            phone = df['Контакты']
            email = df['Почта']
            generates = self.generate()
            data = []
            for i in range(len(birthday)):
                birthday_enter = birthday[i].replace(" ", ".")
                password = "12345678"
                check = json.loads(requests.get(f"{url}/does_exist_pair?name={name[i]}&birthdate={birthday_enter}").text)
                print(check)
                if check is not None:
                    account = get_account(check)
                    generates = check
                    password = "Уже есть"
                else:
                    generates = self.generate()

                data.append(
                        [f"{generates}", f"{name[i]}", f'{birthday_enter}', f"{password}", f"{name_parents[i]}",
                            f"{phone[i]}", f"{email[i]}"])

            birthday_list = []
            id_list = []
            name_list = []
            enter_list = []
            password_list = []
            for i in  range(len(data)):
                id_list.append(data[i][0])
                name_list.append(data[i][1])
                birthday_list.append(data[i][2])
                password_list.append(data[i][3])
            enter_list.append(["ID", id_list])
            enter_list.append(["ФИО", name_list])
            enter_list.append(["Дата рождение", birthday_list])
            enter_list.append(["Пароль", password_list])
            enter_list = dict(enter_list)
            df = pandas.DataFrame(enter_list)
            df.to_excel('./list_user.xlsx')
            self.table_create(data)

        except KeyError:
            toast("Неправильные столбцы")

    @mainthread
    def table_create(self, data):
        self.charge_contests = MDDataTable(
            size_hint=(0.9, 1),
            rows_num=len(data),
            column_data=[
                ("ID", dp(10)),
                ("ФИО", dp(52)),
                ("Дата рождения", dp(19)),
                ("Пароль", dp(19.2)),
                ("Родители", dp(52)),
                ("Контакты", dp(25)),
                ("Почта", dp(45)),
            ],
            row_data=[
                [
                    f"{data[i][0]}",
                    f"{data[i][1]}",
                    f"{data[i][2]}",
                    f"{data[i][3]}",
                    f"{data[i][4]}",
                    f"{data[i][5]}",
                    f"{data[i][6]}",
                ] for i in range(len(data))
            ],
        )
        self.root.ids.generate_table.add_widget(self.charge_contests)
        toast(f"{self.path}")
        self.root.ids.boxlayout_download.pos_hint = ({"center_x": .3, "center_y": .1})
        self.fg = MDRaisedButton(
            id="rr",
            text='Создать пользователей',
            pos_hint=({"center_x": .7, "center_y": .1}),
            on_release=lambda x: self.create_users_sql()

        )
        self.root.ids.boxlayout.add_widget(self.fg)

    def create_users_sql(self):
        for i in range(len(self.charge_contests.row_data)):
            if self.charge_contests.row_data[i][3] == "Уже есть":
                toast("Aккаунт создан")
            else:
                values = [self.charge_contests.row_data[i][0], self.charge_contests.row_data[i][3], self.charge_contests.row_data[i][1], self.charge_contests.row_data[i][2]]
                json = kvant_lib.create_user(self.charge_contests.row_data[i][0], self.charge_contests.row_data[i][1], self.charge_contests.row_data[i][2], "12345678", self.root.ids.login.text,
                                             self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
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
            with open("./list_user.xlsx", "rb") as f:
                a = f.read()
                json = kvant_lib.send_mail(self.dialog_for_send.content_cls.ids.email_for_send.text, a, self.root.ids.login.text, self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            self.screen("teacher_screen")
            self.dialog_close("dialog_for_send")

    def search_students(self, text=""):
        if len(text) >= 4:
            a = time.time()
            self.root.ids.container.clear_widgets()
            LIST = search(json.loads(requests.get(f"{url}/get_account_skeleton_list").text), text)
            print(a-time.time())
            # FAST
            for i in LIST:
                puple = get_account(i)
                self.root.ids.container.add_widget(
                    ThreeLineIconListItem(
                        text=puple['name'],
                        secondary_text=puple['birthdate'],
                        tertiary_text=f"ID: {puple['id']}",
                        on_release=lambda x: self.dialog_windows(x)
                    ),
                )
            print(a-time.time())


    def dialog_windows(self, task_windows):
        print(task_windows.text, task_windows.secondary_text)
        self.name = task_windows.text
        self.birthday = task_windows.secondary_text
        self.id = task_windows.tertiary_text
        balance = balance_def(f"{self.id}")
        if self.dialog_list:
            self.dialog_list = None
        if not self.dialog_list:
            self.dialog_list = MDDialog(
                title=f"{self.name}",
                text=f"Баланс: {balance}",
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

    def dialog_close(self, a):
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
                        on_release=lambda x: self.clear_account()
                    ),
                ],
            )
        self.dialog_confirmation.open()

    def clear_account(self):
        id = self.id.replace("ID: ", "")
        if self.dialog_confirmation.text == "Все данные о пользователе будут стерты безвозратно":
            json = kvant_lib.delete_user(id, self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            toast("Аккаунт удален")
        else:
            json = kvant_lib.change_password(id, "12345678",self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            toast("Пароль сброшен")
        self.dialog_close("dialog_confirmation")
        self.dialog_close("dialog_list")
        self.root.ids.container.clear_widgets()

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
        sum = int(self.dialog_change.content_cls.ids.first_field.text)
        balance = balance_def(self.id)
        print(self.id)
        id = self.id.replace("ID: ", "")
        if confirm == "Списание":
            if balance < sum:
                toast("Недостаточно средст")
            else:
                json = kvant_lib.change_balance(-sum, id, self.dialog_change.content_cls.ids.secondary_field.text, self.root.ids.login.text, self.root.ids.password.text)
                requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
                toast("Списано")
                self.dialog_close("dialog_change")
        elif confirm == "Начислить":
            json = kvant_lib.change_balance(sum, id, self.dialog_change.content_cls.ids.secondary_field.text, self.root.ids.login.text, self.root.ids.password.text)
            requests.post(url=f"{url}/execute", data=json.encode("utf-8"))
            toast("Начислино")
            self.dialog_close("dialog_change")

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

    def send_report(self):
        if len(self.dialog_report_open.content_cls.ids.email_field.text) == 0:
            return toast("Введите почту")
        toast("Отчет придет в течении минуты")
        threading.Thread(target=self.threading_report).start()
        self.dialog_close("dialog_report_open")
        self.dialog_close("dialog_confirmation_report")

    def dialog_connections(self):
        if not self.dialog_lan:
            self.dialog_lan = MDDialog(
                radius=[20, 7, 20, 7],
                title="Изменить сервер",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="url_field",
                        hint_text="URL",
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="60dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="Отмена",
                        on_release=lambda x: self.dialog_close("dialog_lan")
                    ),
                    MDFlatButton(
                        text="Изменить",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.lan_connections()
                    ),
                ],

            )
        self.dialog_lan.open()

    def lan_connections(self):
        print(self.dialog_lan.content_cls.ids.url_field.text)
        toast("Отчет придет в течении минуты")
        self.dialog_close("dialog_report_open")

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
                ))


        self.root.ids.balance_user.text = f"{balance_def(login)} Kvant"

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

                self.screen("login_screen")
                toast("Создали аккаунт")

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
        pass

    def settings_password(self):
        requests.get(f"{url}/passwd?login={self.root.ids.login.text}&new_password={hashlib.sha256(self.dialog_settings_account.content_cls.ids.password_input.text.encode()).hexdigest()}")
        self.dialog_close("dialog_settings_account")

    def log_in(self):
        login = self.root.ids.login.text
        password = self.root.ids.password.text
        check = requests.get(f"{url}/check_login_credentials?login={login}&password={hashlib.sha256(password.encode()).hexdigest()}").text
        print(f"The check is: {check}")
        check = json.loads(check)
        if check:
            account = get_account(login)
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
                self.root.ids.screen_manager.current = "admin_screen"
                self.root.ids.admin_name.text = account["name"]
            if password == "12345678":
                self.dialog_settings_accounts()
        else:
            toast("Введены неверные данные")

    def screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name

    def threading_report(self):
        a = json.loads(requests.get("https://roughy-precious-neatly.ngrok-free.app/get_raiting_skeleton").text)
        sorted_dict = dict(sorted(a.items(), key=lambda item: item[1], reverse=True))
        name_list = []
        rating_list = []
        enter_list = []
        for i in sorted_dict.keys():
            name_list.append(i)
            rating_list.append(sorted_dict[i])
        enter_list.append(["ФИО", name_list])
        enter_list.append(["Рейтинг", rating_list])
        enter_list = dict(enter_list)
        df = pandas.DataFrame(enter_list)
        df.to_excel('./rating_list.xlsx')

        with open("./rating_list.xlsx", "rb") as f:
            a = f.read()
            send = kvant_lib.send_mail(self.dialog_report_open.content_cls.ids.email_field.text, a,
                                       self.root.ids.login.text, self.root.ids.password.text)
            print(self.dialog_report_open.content_cls.ids.email_field.text)
            requests.post(url=f"{url}/execute", data=send.encode("utf-8"))

    def confirmation_report(self):
        if not self.dialog_confirmation_report:
            self.dialog_confirmation_report = MDDialog(
                title=f"Вы точно хотите отправить отчет?",
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
                        on_release=lambda x: self.dialog_report()
                    ),
                ],
            )
        self.dialog_confirmation_report.open()

if __name__ == "__main__":
    MoneyTest().run()
