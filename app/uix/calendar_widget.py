from kivymd.uix.widget import MDWidget
from kivymd.uix.textfield import MDTextFieldHintText,MDTextFieldHelperText,MDTextFieldTrailingIcon
from kivymd.uix.pickers import MDDockedDatePicker
from datetime import date,datetime
from core import DataReader

class CalendarWidget(MDWidget):

    def __init__(self, screen, field, topic_field, text_input, **kwargs):
        super().__init__(**kwargs)
        self.number_of_docked_dates = 0
        self.size_hint = (1, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.current_date = datetime.now().strftime('%d/%m/%Y')
       
        field.add_widget(MDTextFieldHintText(text=self.current_date))
        field.bind(focus= lambda passed_field,focus: self.show_date_picker(passed_field, focus, topic_field, text_input))




    def _on_ok(self, instance_date_picker, field, topic_field, text_input):
        date = instance_date_picker.get_date()[0]
        date_str = str(date).split("-")
        today = datetime.now()
        if date > today.date():
            new_date = today.strftime('%d/%m/%Y')
        else:
            new_date = f"{date_str[2]}/{date_str[1]}/{date_str[0]}"

        text_field = MDTextFieldHintText(text=new_date)
        field.text = new_date
        field.add_widget(text_field)
        field.focus = True
        data_reader = DataReader()
        data_reader.load_data(topic_field, text_input,new_date)
        instance_date_picker.dismiss()
        field.focus = False
        self.number_of_docked_dates -= 1



    def _on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()
        self.number_of_docked_dates -= 1

    def show_date_picker(self, field, focus, topic_field, text_input):
        if not focus:
            return
        if self.number_of_docked_dates == 0:

            self.number_of_docked_dates += 1
            today = date.today()
            date_dialog = MDDockedDatePicker(year=today.year, month = today.month, day=today.day)
            date_dialog.min_year = 2000
            date_dialog.max_year = today.year +1
            
            date_dialog.bind(on_ok= lambda date_picker: self._on_ok(date_picker, field, topic_field, text_input))
            date_dialog.bind(on_cancel=self._on_cancel)
            date_dialog.open()