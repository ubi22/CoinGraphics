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
from kivy.uix.boxlayout import BoxLayout
Window.size = (520, 900)


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MoneyTest(MDApp):

    def notification(self):
        self.root.ids.notification_bell.icon = 'bell-ring'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            size_hint=(0.7, 0.6),
            use_pagination=True,
            check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("No.", dp(30), None, "Custom tooltip"),
                ("Status", dp(30)),
                ("Signal Name", dp(60)),
                ("Severity", dp(30)),
                ("Stage", dp(30)),
                ("Schedule", dp(30), lambda *args: print("Sorted using Schedule")),
                ("Team Lead", dp(30)),
            ],
        )
        layout.add_widget(self.data_tables)
        return Builder.load_file("kivy.kv")

    def copy_button_text(self):
        Clipboard.copy(self.root.ids.id_users.text)

    def screen(self, screen_name: str):
        self.root.ids.screen_manager.current = screen_name

    def login_main_page(self):
        if not self.root.ids.login.text == "admin":
            self.screen("admin_screen")
        else:
            self.screen("main_screen")


app = MoneyTest()
app.run()
