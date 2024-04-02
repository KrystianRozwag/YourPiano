from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.uix.anchorlayout import MDAnchorLayout
from uix import TunerScreen, SettingsScreen, SheetsScreen, CalendarScreen
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.theme_cls.primary_palette = "Teal"
        self.md_bg_color = self.theme_cls.backgroundColor
        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='center')
        layout = MDBoxLayout(orientation='horizontal', spacing=10, padding=10)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        settings_btn = MDButton(MDButtonText(text="Settings"), 
                     size_hint=(None, None))
        calendar_btn = MDButton(MDButtonText(text="Calendar"), 
                     size_hint=(None, None))
        tuner_btn = MDButton(MDButtonText(text="Tuner"), 
                     size_hint=(None, None))
        sheets_btn = MDButton(MDButtonText(text="Sheets"),
                     size_hint=(None, None))

        buttons_bind = {settings_btn:self.change_to_settings, calendar_btn:self.change_to_calendar , tuner_btn:self.change_to_tuner ,sheets_btn:self.change_to_sheets }
        for btn_name,btn_func in buttons_bind.items():
            layout.add_widget(btn_name)
            btn_name.bind(on_press=btn_func)

        anchor_layout.add_widget(layout)

        self.add_widget(anchor_layout)

    def change_to_settings(self, *args):
        if not self.parent.has_screen('settings'):
            self.parent.add_widget(SettingsScreen(name='settings'))
        self.manager.current = 'settings'

    def change_to_tuner(self, *args):
        if not self.parent.has_screen('tuner'):
            self.parent.add_widget(TunerScreen(name='tuner'))
        self.manager.current = 'tuner'

    def change_to_calendar(self, *args):
        if not self.parent.has_screen('calendar'):
            self.parent.add_widget(CalendarScreen(name='calendar'))
        self.manager.current = 'calendar'

    def change_to_sheets(self, *args):
        if not self.parent.has_screen('sheets'):
            self.parent.add_widget(SheetsScreen(name='sheets'))
        self.manager.current = 'sheets'