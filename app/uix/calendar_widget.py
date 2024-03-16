from kivymd.uix.widget import MDWidget
from kivymd.uix.textfield import MDTextField,MDTextFieldHintText,MDTextFieldHelperText,MDTextFieldTrailingIcon
from kivy.metrics import dp
from kivymd.uix.pickers import MDDockedDatePicker
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from datetime import date,datetime
from kivy.core.window import Window
import os


class CalendarWidget(MDWidget):

    def __init__(self, screen, field, **kwargs):
        super().__init__(**kwargs)
        self.number_of_docked_dates = 0
        self.size_hint = (1, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.current_date = datetime.now().strftime('%d/%m/%Y')
        #self.calendar_field = MDTextField(
         #   MDTextFieldHelperText(text="DD/MM/YYYY",mode="persistent"),
          #  MDTextFieldTrailingIcon(icon="calendar"),
           # date_format = "dd/mm/yyyy",
            #text = self.current_date,
            #id="calendar_field",
            #validator="date",
            #mode="outlined",
            #size_hint=(1, None), height='48dp'
        #)
        field.add_widget(MDTextFieldHintText(text=self.current_date))
        field.bind(focus= lambda passed_field,focus: self.show_date_picker(passed_field, focus))

       # self.add_widget(self.calendar_field)


  #  def get_calendar_field(self):
   #     return self.calendar_field
    
    def on_ok(self, instance_date_picker, field):

        date = str(instance_date_picker.get_date()[0]).split("-")
        new_date = f"{date[2]}/{date[1]}/{date[0]}"
        text_field = MDTextFieldHintText(text=new_date)
        field.text = new_date
        field.add_widget(text_field)
        field.focus = True

        instance_date_picker.dismiss()
        field.focus = False
        self.number_of_docked_dates -= 1



    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()
        self.number_of_docked_dates -= 1

    def show_date_picker(self, field, focus):
        if not focus:
            return
        if self.number_of_docked_dates == 0:

            self.number_of_docked_dates += 1
            today = date.today()
            date_dialog = MDDockedDatePicker(year=today.year, month = today.month, day=today.day)

            date_dialog.bind(on_ok= lambda date_picker: self.on_ok(date_picker, field))
            date_dialog.bind(on_cancel=self.on_cancel)
            date_dialog.open()