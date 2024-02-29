from uix import TunerScreen, SettingsScreen, SheetsScreen, CalendarScreen
from functools import partial
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 0, 0, 1)  # Red color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        layout = BoxLayout(orientation='horizontal', size_hint=(None, None), padding=10, spacing=10)

        settings_btn = Button(text="Settings", 
                     background_color=(1,0,0,1),
                     size_hint=(None, None), size=(100, 50))
        calendar_btn = Button(text="Calendar", 
                     background_color=(1,0,0,1),
                     size_hint=(None, None), size=(100, 50))
        tuner_btn = Button(text="Tuner", 
                     background_color=(1,0,0,1),
                     size_hint=(None, None), size=(100, 50))
        sheets_btn = Button(text="Sheets", 
                     background_color=(1,0,0,1),
                     size_hint=(None, None), size=(100, 50))
        
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

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class ScreensManager(ScreenManager):
    pass

class PianoDiaryApp(App):
    def build(self):
        sm = ScreensManager()
        screens = [MainScreen(name='main'),CalendarScreen(name='calendar'),SheetsScreen(name='sheets'),TunerScreen(name='tuner'), SettingsScreen(name='settings')]
        for widget in screens:
            sm.add_widget(widget)
        return sm
        

if __name__ == '__main__':
    PianoDiaryApp().run()