from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText,BaseButton
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
from mido import MidiFile, MidiTrack, Message, open_input
import time
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
        box = MDBoxLayout(orientation='horizontal', spacing=5, padding=1,size_hint=(1, 0.2))
        record_box = MDBoxLayout(orientation='horizontal', spacing=5, padding=1,size_hint=(0.5, 0.1))
        back_btn = MDButton(MDButtonText(text="Menu"), 
                     size_hint=(None, None), size=(100, 50))
        record_btn = MDButton(MDButtonText(text="Record"), 
                     size_hint=(None, None), size=(100, 50))
        stop_btn = MDButton(MDButtonText(text="Stop"), 
                     size_hint=(None, None), size=(100, 50))
        

        for input in mido.get_input_names():
            if "Digital Piano" in input:
                self.inport = mido.open_input(input)
                break
            listener_thread = threading.Thread(target=self.midi_listener, daemon=True)
            listener_thread.start()

        for note in range(48, 72):  # MIDI notes from C3 to B4
            note_name = self.get_note_name(note)
            button = MDButton(MDButtonText(text=note_name), pos_hint={"center_x": .5}, height="100px",width="5px",md_bg_color=self.theme_cls.surfaceColor)
            if note % 2 == 0:
                button.md_bg_color = (1,1,1,1)
            self.note_buttons[note] = button
            box.add_widget(button)

        back_btn.bind(on_press=self.back_to_menu)
        record_btn.bind(on_press=lambda *args: self.start_recording(self.inport))
        stop_btn.bind(on_press=self.back_to_menu)
        record_box.add_widget(record_btn)
        record_box.add_widget(stop_btn)
        record_layout.add_widget(record_box)
        anchor_layout.add_widget(back_btn)
        box_anchor_layout.add_widget(box)
        self.add_widget(anchor_layout)
        self.add_widget(record_layout)
        self.add_widget(box_anchor_layout)
    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
            self.save_midi('recorded_midi.mid')
            self.record_btn.text = "Start Recording"
        else:
            self.start_recording(self.inport)
            self.record_btn.text="Stop Recording"
    def start_recording(self, port_name):
        if not self.recording:
            self.recording = True
            self.recorded_messages = []
            self.start_time = time.time()
            self.inport = mido.open_input(port_name)
            self.thread = threading.Thread(target=self.record)
            self.thread.start()
            print("Recording started.")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.thread.join()
            self.inport.close()
            print("Recording stopped.")

    def record(self):
        while self.recording:
            for msg in self.inport.iter_pending():
                timestamp = time.time() - self.start_time
                msg.time = timestamp
                self.recorded_messages.append(msg)
                print(msg)

    def save_midi(self, filename):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        for msg in self.recorded_messages:
            track.append(msg)

        mid.save(filename)
        print(f"Saved to {filename}")

    def record_message(self):
        if self.inport:
            print(f"Recording from {self.inport}. Press Ctrl+C to stop.")
            
            recorded_messages = []
            start_time = time.time()
            
            try:
                for msg in self.inport:
                    # Capture the time since recording started
                    timestamp = time.time() - start_time
                    # Add a time attribute to the message
                    msg.time = timestamp
                    recorded_messages.append(msg)
                    print(msg)
            except KeyboardInterrupt:
                print("Recording stopped.")
            self.save_midi(recorded_messages)

        # Optionally, save the recorded messages to a MIDI file


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