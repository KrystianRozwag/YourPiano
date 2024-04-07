from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel 
from core import MidiHandler
class SheetsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SheetsScreen, self).__init__(**kwargs)
        self.inport = ""
        self.note_to_label = {}
        self.note_buttons = {}
        self.recording = False
        self.theme_cls.primary_palette = "Olive"
        self.md_bg_color = self.theme_cls.backgroundColor
        
        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='bottom')
        box_anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='center')
        record_layout = MDAnchorLayout(anchor_x='center', anchor_y='top')

        self.box = MDBoxLayout(orientation='horizontal', spacing=5, padding=1,size_hint=(1, 0.2))
        record_box = MDBoxLayout(orientation='horizontal', spacing=5, padding=5,size_hint=(0.5, 0.1))

        back_btn = MDButton(MDButtonText(text="Menu"), 
                     size_hint=(None, None), size=(100, 50))
        self.record_btn = MDButton(MDButtonText(text="Record"), 
                     size_hint=(None, None), size=(100, 50))
        #stop_btn = MDButton(MDButtonText(text="Stop"), 
         #            size_hint=(None, None), size=(100, 50))
        self.connect_btn = MDButton(MDButtonText(text="Connect"), 
                     size_hint=(None, None), size=(100, 50))
        self.connection_message = MDLabel(text="", halign="center")
        

       
        self.create_notes()
        midi_handler = MidiHandler(self.note_buttons)
        back_btn.bind(on_press=self.back_to_menu)
        self.record_btn.bind(on_press=lambda *args: midi_handler.toggle_recording(self.record_btn))
        self.connect_btn.bind(on_press=lambda *args: midi_handler.connect_device(self.connection_message, self.record_btn))
        #stop_btn.bind(on_press=self.back_to_menu)
        record_box.add_widget(self.connect_btn)
        record_box.add_widget(self.record_btn)
        #record_box.add_widget(stop_btn)
        record_box.add_widget(self.connection_message)
        record_layout.add_widget(record_box)
        anchor_layout.add_widget(back_btn)
        box_anchor_layout.add_widget(self.box)
        self.add_widget(anchor_layout)
        self.add_widget(record_layout)
        self.add_widget(box_anchor_layout)

    def __add_widgets__(self):
        pass
   
    def create_notes(self):
         for note in range(48, 72):  # MIDI notes from C3 to B4
            note_name = self.get_note_name(note)
            button = MDButton(
                #MDButtonText(text=note_name), 
                              pos_hint={"center_x": .5}, 
                              height="100px",
                              width="40px",
                              theme_bg_color = "Custom", 
                              md_bg_color="white",
                              radius = [5,5,5,5]
                              )
            if note % 2 != 0:
                button.md_bg_color = (0,0,0,1)
                button.width="20px"
            self.note_buttons[note] = button
            self.box.add_widget(button)
    def get_note_name(self, midi_note):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_note // 12) - 1
        note_index = midi_note % 12
        return note_names[note_index] + str(octave)

    def back_to_menu(self, *args):
        self.manager.current = 'main'
        if self.manager.has_screen('sheets'):
            self.manager.remove_widget(self.manager.get_screen('sheets'))