from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screenmanager import MDScreenManager
import mido
import threading
#from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
from kivy.clock import Clock
from music21 import pitch
class SheetsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SheetsScreen, self).__init__(**kwargs)
        #self.theme_cls.primary_palette = "Olive"
        self.md_bg_color = self.theme_cls.backgroundColor
        anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='bottom')
        box_anchor_layout = MDAnchorLayout(anchor_x='center', anchor_y='center')
        box = MDBoxLayout(orientation='horizontal', spacing=5, padding=1,size_hint=(1, 0.2))
        back_btn = MDButton(MDButtonText(text="Menu"), 
                     size_hint=(None, None), size=(100, 50))
        
        back_btn.bind(on_press=self.back_to_menu)
        anchor_layout.add_widget(back_btn)
        self.add_widget(anchor_layout)
        print(mido.get_input_names())
        self.inport = mido.open_input('Digital Piano-1 0')
        listener_thread = threading.Thread(target=self.midi_listener, daemon=True)
        listener_thread.start()
        self.note_to_label = {}
        self.note_buttons = {}
        for note in range(48, 72):  # MIDI notes from C3 to B4
            note_name = self.get_note_name(note)
            button = MDButton(MDButtonText(text=note_name), pos_hint={"center_x": .5}, height="100px",width="30px")
            self.note_buttons[note] = button
            box.add_widget(button)
        box_anchor_layout.add_widget(box)
        self.add_widget(box_anchor_layout)



    def get_note_name(self, midi_note):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_note // 12) - 1
        note_index = midi_note % 12
        return note_names[note_index] + str(octave)

    def highlight_note(self,note, action, velocity):
        if note in self.note_buttons:
            button = self.note_buttons[note]
            if velocity == 64:
                button.md_bg_color = (1,0,0,1) # Red
                button.style = "filled"
            else:
                button.md_bg_color = (0.1,0,0,1)
                button.style = "elevated"

    def handle_midi_message(self,message):
        if message.type in ['note_on', 'note_off']:
            self.highlight_note(message.note, message.type, message.velocity)

    def midi_listener(self):
        for message in self.inport:
                print(message)
                self.handle_midi_message(message)
            

    def back_to_menu(self, *args):
        self.manager.current = 'main'