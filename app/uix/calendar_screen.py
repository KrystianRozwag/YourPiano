from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screenmanager import MDScreenManager
from uix.calendar_widget import CalendarWidget
from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivy.metrics import dp
from kivymd.uix.pickers import MDDockedDatePicker
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from datetime import date
KV = '''
MDTextField:
    id: field
    mode: "outlined"
    pos_hint: {'center_x': .5, 'center_y': .85}
    size_hint_x: .5
    on_focus: app.root.get_screen('calendar').show_date_picker(self.focus) if self.focus else None

    MDTextFieldHintText:
        text: app.current_date

    MDTextFieldHelperText:
        text: "MM/DD/YYYY"
        mode: "persistent"

    MDTextFieldTrailingIcon:
        icon: "calendar"
'''


class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        today = date.today()
        self.theme_cls.primary_palette = "Olive"
        self.md_bg_color = self.theme_cls.backgroundColor
        date_dialog = MDDockedDatePicker(year=today.year, month = today.month, day=today.day)
        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='bottom')
        back_btn = MDButton(MDButtonText(text="Menu"), 
                    size_hint=(None, None), size=(100, 50))
        back_btn.bind(on_press= lambda instance: self.back_to_menu(date_dialog))

        anchor_layout.add_widget(back_btn)
        self.add_widget(anchor_layout)
        self.add_widget(Builder.load_string(KV))
        


    def on_ok(self, instance_date_picker):
        print(instance_date_picker.get_date()[0])  
        
    def show_date_picker(self, focus):
        if not focus:
            return
        
        date_dialog = MDDockedDatePicker()
        # You have to control the position of the date picker dialog yourself.
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.open()
        
        
    def back_to_menu(self, date_dialog):
#        date_dialog.dismiss()
        self.manager.current = 'main'




