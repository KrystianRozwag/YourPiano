from uix import MainScreen, TunerScreen, SettingsScreen, SheetsScreen, CalendarScreen
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

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