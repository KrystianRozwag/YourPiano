from kivymd.uix.textfield import MDTextField,MDTextFieldHintText,MDTextFieldHelperText,MDTextFieldTrailingIcon


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
from datetime import date,datetime
import json

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

number_of_docked_dates = 0
class CalendarScreen(MDScreen):

    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)

        self.theme_cls.primary_palette = "Olive"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.current_date = datetime.now().strftime('%d/%m/%Y')

        calendar_field = MDTextField(
            MDTextFieldHelperText(text="DD/MM/YYYY",mode="persistent"),
            MDTextFieldTrailingIcon(icon="calendar"),
            date_format = "dd/mm/yyyy",
            validator="date",
            mode="outlined",
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            size_hint_x=0.5
        )
        calendar_field.add_widget(MDTextFieldHintText(text=self.current_date))
        calendar_field.bind(focus= lambda passed_field,focus: self.show_date_picker(passed_field, focus))
        calendar_field.set_pos_hint_text(0,0)
        self.add_widget(calendar_field)
        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='center')
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=10,size_hint=(0.5, None))
        anchor_layout_btns = MDAnchorLayout(anchor_x='center', anchor_y='bottom')
        topic_field =  MDTextField(
            MDTextFieldHintText(text="Topic"),
            pos_hint={'center_x': 0.5, 'center_y': 1},
            size_hint_x=0.5
        )
        description_field =  MDTextField(
            MDTextFieldHintText(text="Description"),
            mode="outlined",
           pos_hint={'center_x': 0.5, 'center_y': 0.8},

        )
        load_file_btn = MDButton(MDButtonText(text="Load file"), 
                    size_hint=(None, None), size=(100, 50),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                    )
        
        back_btn = MDButton(MDButtonText(text="Menu"), 
                    size_hint=(None, None), size=(100, 50))
        back_btn.bind(on_press=self.back_to_menu)
        load_file_btn.bind(on_press=lambda *args: self.send_data(calendar_field) )

        layout.add_widget(topic_field)
        layout.add_widget(description_field)
        layout.add_widget(load_file_btn)

        anchor_layout_btns.add_widget(back_btn)
        anchor_layout.add_widget(layout)

        self.add_widget(anchor_layout)
        self.add_widget(anchor_layout_btns)
        

    def load_json():
        pass

    def send_data(self, calendar_field):
        with open('app\\assets\\data\\notes.json','r') as json_file:
            data = json.load(json_file)
        
            notes = data['notes']
            for note in notes:
                date = note['date']
                title = note['title']
                description = note['description']
                filePath = note['filePath']
                print(date)

        
    def on_ok(self, instance_date_picker, field):
        global number_of_docked_dates
        text_field = MDTextFieldHintText(text=str(instance_date_picker.get_date()[0]))
        field.add_widget(text_field)
        field.focus = True

        instance_date_picker.dismiss()
        field.focus = False
        number_of_docked_dates -= 1



    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()

    def show_date_picker(self, field, focus):
        global number_of_docked_dates
        if not focus:
            return
        if  number_of_docked_dates == 0:
            number_of_docked_dates += 1
            today = date.today()
            date_dialog = MDDockedDatePicker(year=today.year, month = today.month, day=today.day)

            # You have to control the position of the date picker dialog yourself.
            #date_dialog.bind(on_select_day=lambda date, day: self.on_ok(date, day, field) )
            date_dialog.bind(on_ok= lambda date_picker: self.on_ok(date_picker, field))
            date_dialog.bind(on_cancel=self.on_cancel)
            date_dialog.open()

        
        
    def back_to_menu(self, value):
#        date_dialog.dismiss()
        self.manager.current = 'main'




