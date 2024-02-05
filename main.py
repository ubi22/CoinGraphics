from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
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
        return Builder.load_file("kivy.kv")

    def copy_button_text(self):
        Clipboard.copy(self.root.ids.id_users.text)

    def screen(self, screen_name: str):
        self.root.ids.screen_manager.current = screen_name

    def login_main_page(self):
        self.screen("main_screen")


app = MoneyTest()
app.run()
