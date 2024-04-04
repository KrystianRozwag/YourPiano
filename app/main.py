from uix import MainScreen
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

class ScreensManager(MDScreenManager):
    pass

class PianoDiaryApp(MDApp):
    def build(self):
        sm = ScreensManager()
        sm.add_widget(MainScreen(name='main')) 
        return sm
        

if __name__ == '__main__':
    PianoDiaryApp().run()