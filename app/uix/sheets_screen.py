from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screenmanager import MDScreenManager
class SheetsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SheetsScreen, self).__init__(**kwargs)
        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='bottom')
        back_btn = MDButton(MDButtonText(text="Menu"), 
                     size_hint=(None, None), size=(100, 50))
        
        back_btn.bind(on_press=self.back_to_menu)
        anchor_layout.add_widget(back_btn)
        self.add_widget(anchor_layout)

    def back_to_menu(self, *args):
        self.manager.current = 'main'