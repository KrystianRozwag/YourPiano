from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivy.metrics import dp
from kivymd.uix.pickers import MDDockedDatePicker



class CalendarWidget(MDWidget):
    def build(self):
        self.theme_cls.primary_palette = "Olive"


    def show_date_picker(self, focus):
        if not focus:
            return

        date_dialog = MDDockedDatePicker()
        # You have to control the position of the date picker dialog yourself.
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        '''Events called when the "OK" dialog box button is clicked.'''
        print("Selected date:", value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        print("Date picker canceled")
