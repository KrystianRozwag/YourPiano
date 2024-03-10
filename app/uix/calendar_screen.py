from kivymd.uix.textfield import MDTextField,MDTextFieldHintText,MDTextFieldHelperText,MDTextFieldTrailingIcon


from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screenmanager import MDScreenManager

from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivy.metrics import dp
from kivymd.uix.pickers import MDDockedDatePicker
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from datetime import date,datetime
import json
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from tkinter import filedialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.core.window import Window
import os
from kivymd.uix.label import MDLabel 
from kivymd.uix.scrollview import MDScrollView
number_of_docked_dates = 0
file_path = ''
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
            text = self.current_date,
            id="calendar_field",
            validator="date",
            mode="outlined",
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            size_hint_x=0.5
        )
        calendar_field.add_widget(MDTextFieldHintText(text=self.current_date))
        calendar_field.bind(focus= lambda passed_field,focus: self.show_date_picker(passed_field, focus))
        calendar_field.set_pos_hint_text(0,0)
        self.add_widget(calendar_field)

        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='bottom')
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=20,size_hint=(0.5, None))
        anchor_layout_btns = MDAnchorLayout(anchor_x='right', anchor_y='bottom', padding=10)
        scroll_view = MDScrollView(size_hint=(1, None), height=200)
        
        # Create a TextInput for multi-line text input
        text_input = TextInput(
            size_hint_y=1,
            multiline=True,
            background_color=(1, 1, 1, 1),  # White background
            pos_hint={'center_x': 0.5, 'center_y': 0.5},

        )
        text_input.bind(minimum_height=text_input.setter('height'))
        topic_field =  MDTextField(
            MDTextFieldHintText(text="Topic"),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            size_hint_x=0.5
        )
        #description_field =  MDTextField(
         #   MDTextFieldHintText(text="Description"),
          #  mode="outlined",
           # pos_hint={'center_x': 0.5, 'center_y': 0.8},
            #multiline=True
        #)
        choose_file_btn = MDButton(MDButtonText(text="Choose file"), 
            size_hint=(None, None), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size=(100, 50),

        )
        load_file_btn = MDButton(MDButtonText(text="Send day"), 
            size_hint=(None, None), 
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        path_label = MDLabel(text="", halign="center")

        back_btn = MDButton(MDButtonText(text="Menu"), 
                    size_hint=(None, None), size=(100, 50))
        
        back_btn.bind(on_press=self.back_to_menu)
        load_file_btn.bind(on_press=lambda *args: self.send_data(calendar_field, topic_field, text_input) )
        choose_file_btn.bind(on_release=lambda *args: self.load_file(path_label))
        scroll_view.add_widget(text_input)
        widgets = [topic_field,scroll_view,choose_file_btn,path_label,load_file_btn]
        for widget in widgets:
            layout.add_widget(widget)

        anchor_layout_btns.add_widget(back_btn)
        anchor_layout.add_widget(layout)

        self.add_widget(anchor_layout)
        self.add_widget(anchor_layout_btns)



    def load_file(self, path_label):
        global file_path
        file_types = [
    ('MP3 files', '*.mp3'),
    ('WAV files', '*.wav'),
    # Add more file types if needed
        ]
        file_path = filedialog.askopenfilename() #filetypes=file_types
        filename = file_path.split("/")
        path_label.text = filename[-1]


    def send_data(self, calendar_field, topic_field, description_field):
        global file_path
        with open('app\\assets\\data\\notes.json','r') as json_file:
            data = json.load(json_file)
       
        notes = data['notes']
        for note in notes:
            if note['date'] == calendar_field.text and topic_field.text == note['title'] and description_field.text == note['description']:
                topic_field.text = note['title']
                description_field.text = note['description']
                return True
            
            elif note['date'] == calendar_field.text and (topic_field.text != note['title'] or description_field.text != note['description']):
                note['title'] = topic_field.text
                note['description'] = description_field.text
                notes.remove(note)
                break

        new_date = {
        "date": calendar_field.text,
        "title": topic_field.text,
        "description": description_field.text,
        "filePath": file_path
        }
        notes.append(new_date)
                    
        with open('app\\assets\\data\\notes.json','w') as json_file:
            json.dump(data, json_file, indent=4)

        
    def on_ok(self, instance_date_picker, field):
        global number_of_docked_dates
        date = str(instance_date_picker.get_date()[0]).split("-")
        new_date = f"{date[2]}/{date[1]}/{date[0]}"
        text_field = MDTextFieldHintText(text=new_date)
        field.text = new_date
        field.add_widget(text_field)
        field.focus = True

        instance_date_picker.dismiss()
        field.focus = False
        number_of_docked_dates -= 1



    def on_cancel(self, instance_date_picker):
        global number_of_docked_dates
        instance_date_picker.dismiss()
        number_of_docked_dates -= 1

    def show_date_picker(self, field, focus):
        global number_of_docked_dates
        if not focus:
            return
        if  number_of_docked_dates == 0:
            number_of_docked_dates += 1
            today = date.today()
            date_dialog = MDDockedDatePicker(year=today.year, month = today.month, day=today.day)

            date_dialog.bind(on_ok= lambda date_picker: self.on_ok(date_picker, field))
            date_dialog.bind(on_cancel=self.on_cancel)
            date_dialog.open()

        
        
    def back_to_menu(self, value):
#        date_dialog.dismiss()
        self.manager.current = 'main'




