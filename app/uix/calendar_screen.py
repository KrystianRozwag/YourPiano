from kivymd.uix.textfield import MDTextField,MDTextFieldHintText,MDTextFieldHelperText,MDTextFieldTrailingIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel 
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.textinput import TextInput
from datetime import datetime
from uix.calendar_widget import CalendarWidget
from tkinter import filedialog
from core import DataSender

class CalendarScreen(MDScreen):

    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)
        self.file_path = ''
        #self.theme_cls.primary_palette = "Olive"
        self.md_bg_color = self.theme_cls.backgroundColor
        self.current_date = datetime.now().strftime('%d/%m/%Y')
        self.size_hint = (1,1)

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
            size_hint_x=0.5,
            required = True
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
        self.send_file_btn = MDButton(MDButtonText(text="Send day"), 
            size_hint=(None, None), 
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            disabled = True
        )
        path_label = MDLabel(text="", halign="center")

        back_btn = MDButton(MDButtonText(text="Menu"), 
                    size_hint=(None, None), size=(100, 50))
        
        self.current_date = datetime.now().strftime('%d/%m/%Y')
        self.calendar_field = MDTextField(
            MDTextFieldHelperText(text="DD/MM/YYYY",mode="persistent"),
            MDTextFieldTrailingIcon(icon="calendar"),
            date_format = "dd/mm/yyyy",
            text = self.current_date,
            id="calendar_field",
            validator="date",
            mode="outlined",
            size_hint=(1, None), 
            height='48dp',
        )
        calendar_widget = CalendarWidget(self, self.calendar_field, topic_field, text_input)
        self.add_widget(calendar_widget)
        back_btn.bind(on_press=self._back_to_menu)
        data_sender = DataSender()
        
        self.send_file_btn.bind(on_press=lambda *args: data_sender.send_data(self.calendar_field, topic_field, text_input, self.file_path) )
        choose_file_btn.bind(on_release=lambda *args: self._load_file(path_label))
        topic_field.bind(set_text=lambda *args: self._block_send_btn())
        scroll_view.add_widget(text_input)
        layout.add_widget(self.calendar_field)
        widgets = [topic_field,scroll_view,choose_file_btn,path_label,self.send_file_btn]
        for widget in widgets:
            layout.add_widget(widget)

        anchor_layout_btns.add_widget(back_btn)

        anchor_layout.add_widget(layout)

        self.add_widget(anchor_layout)
        self.add_widget(anchor_layout_btns)


    def _block_send_btn(self):
        if self.topic_field.text != "":
            self.send_file_btn.disabled = False
        else:
            self.send_file_btn.disabled = True
            
    def _load_file(self, path_label):
        file_types = [
    ('MP3 files', '*.mp3'),
    ('WAV files', '*.wav'),
    # Add more file types if needed
        ]
        self.file_path = filedialog.askopenfilename() #filetypes=file_types
        filename = self.file_path.split("/")
        path_label.text = filename[-1]

    def _back_to_menu(self, value):
        self.manager.current = 'main'
        if self.manager.has_screen('calendar'):
            self.manager.remove_widget(self.manager.get_screen('calendar'))




