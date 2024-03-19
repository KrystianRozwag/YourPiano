from uix import TunerScreen, SettingsScreen, SheetsScreen, CalendarScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screenmanager import MDScreenManager
from datetime import datetime
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.theme_cls.primary_palette = "Teal"
        self.md_bg_color = self.theme_cls.backgroundColor
        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='center')
        layout = MDBoxLayout(orientation='horizontal', spacing=10, padding=10)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        settings_btn = MDButton(MDButtonText(text="Settings"), 
                     size_hint=(None, None))
        calendar_btn = MDButton(MDButtonText(text="Calendar"), 
                     size_hint=(None, None))
        tuner_btn = MDButton(MDButtonText(text="Tuner"), 
                     size_hint=(None, None))
        sheets_btn = MDButton(MDButtonText(text="Sheets"),
                     size_hint=(None, None))

        buttons = {'settings':settings_btn, 'calendar':calendar_btn, 'tuner':tuner_btn,'sheets':sheets_btn}
        for key,value in buttons.items():
            layout.add_widget(value)

        settings_btn.bind(on_press=self.change_to_settings)
        calendar_btn.bind(on_press=self.change_to_calendar)
        tuner_btn.bind(on_press=self.change_to_tuner)
        sheets_btn.bind(on_press=self.change_to_sheets)
        anchor_layout.add_widget(layout)

        self.add_widget(anchor_layout)

    def change_to_settings(self, *args):
        self.manager.current = 'settings'

    def change_to_tuner(self, *args):
        self.manager.current = 'tuner'

    def change_to_calendar(self, *args):
        self.manager.current = 'calendar'

    def change_to_sheets(self, *args):
        self.manager.current = 'sheets'


class ScreensManager(MDScreenManager):
    pass

class PianoDiaryApp(MDApp):
    def build(self):
        sm = ScreensManager()
        screens = [MainScreen(name='main'),CalendarScreen(name='calendar'),SheetsScreen(name='sheets'),TunerScreen(name='tuner'), SettingsScreen(name='settings')]
        for widget in screens:
            sm.add_widget(widget)
        return sm
        

if __name__ == '__main__':
    PianoDiaryApp().run()