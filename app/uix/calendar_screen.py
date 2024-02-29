from functools import partial
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
#from uix.piano_keyboard_widget import KeyboardWidget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        back_btn = Button(text="Menu", 
                     background_color=(1,0,0,1),
                     size_hint=(None, None), size=(100, 50))
        
        back_btn.bind(on_press=self.back_to_menu)
        anchor_layout.add_widget(back_btn)
        self.add_widget(anchor_layout)

    def back_to_menu(self, *args):
        self.manager.current = 'main'
