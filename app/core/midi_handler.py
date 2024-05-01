from mido import MidiFile, MidiTrack
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
import time
from datetime import datetime
import mido
import threading

class ValueCheckbox(MDCheckbox):
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value

class MidiHandler:
    def __init__(self, note_buttons, record_btn_txt):
        self.recording = False
        self.inport = ""
        self.note_buttons = note_buttons
        self.selected_port = ""
        self.record_btn_txt = record_btn_txt

    def find_device(self, connect_message, record_btn, record_box):
        input_devices = mido.get_input_names()
        if(len(input_devices)==0):
            connect_message.text = "No devices connected"
            return 0
        
        for input in mido.get_input_names():
            ''' if "Digital Piano" in input:
                self.inport = mido.open_input(input)
                connect_message.text = "Connection Success to " + str(self.inport)
                self.listener_thread = threading.Thread(target=self.midi_listener, daemon=True)
                self.listener_thread.start()
                record_btn.disabled = False
                return input'''
            checkbox = ValueCheckbox(group="connections", value = input)
            checkbox.bind(on_touch_down=lambda *args: self._assign_port(checkbox.value))
            record_box.add_widget(checkbox)
            status_label = MDLabel(text=input)
            record_box.add_widget(status_label)
        
        connect_btn = MDButton(MDButtonText(text="Connect"), 
                     size_hint=(None, None), size=(100, 50))
        connect_btn.bind(on_press=lambda *args: self._connect_device(connect_message, record_btn))
        record_box.add_widget(connect_btn)

    def _connect_device(self, connect_message, record_btn):
                self.inport = mido.open_input(self.selected_port)
                connect_message.text = "Connection Success to " + str(self.inport)
                self.listener_thread = threading.Thread(target=self.midi_listener, daemon=True)
                self.listener_thread.start()
                record_btn.disabled = False
                return input

    def _assign_port(self, checkbox_value):
        self.selected_port = checkbox_value

    def toggle_recording(self, record_btn):
        if self.recording:
            self.stop_recording()
            now = datetime.now()
            dt_string =  now.strftime("%d-%m-%Y %H-%M-%S") + " - midi.mid"
            self.save_midi(dt_string)
            record_btn.remove_widget(self.record_btn_txt)
            self.record_btn_txt = MDButtonText(text="Start Recording")
            record_btn.add_widget(self.record_btn_txt)

        else:
            record_btn.remove_widget(self.record_btn_txt)
            self.record_btn_txt = MDButtonText(text="Stop Recording")
            record_btn.add_widget(self.record_btn_txt)
            self.start_recording(self.inport)


    def start_recording(self, port_name):
        if not self.recording:
            self.recording = True
            self.recorded_messages = []
            self.start_time = time.time()
            #self.inport = mido.open_input(port_name)
            self.thread = threading.Thread(target=self.record)
            self.thread.start()
            print("Recording started.")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            #self.thread.join()
            self.inport.close()
            print("Recording stopped.")

    def record(self):
        while self.recording:
            for msg in self.inport:
                if msg.is_realtime:
                    # Skip realtime messages
                    continue
                timestamp = time.time() - self.start_time
                ticks_per_second = 120 / 60 * 480
                ticks = int(timestamp * ticks_per_second)
                # Add a time attribute to the message
                msg.time = ticks
                self.recorded_messages.append(msg)
                print(msg)

    def save_midi(self, filename):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        last_tick = 0
        for msg in self.recorded_messages:
         #   track.append(mido.second2tick(msg.time, mid.ticks_per_beat,500000))
            delta_ticks = msg.time - last_tick
            # Set the message time to the delta time
            msg.time = delta_ticks
            track.append(msg)
            last_tick = msg.time

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

    def midi_listener(self):
        for message in self.inport:
                print(message)
                self.handle_midi_message(message)

                
    def handle_midi_message(self,message):
        if message.type in ['note_on', 'note_off']:
           self.highlight_note(message.note, message.type, message.velocity)

    def get_note_name(self, midi_note):
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_note // 12) - 1
        note_index = midi_note % 12
        return note_names[note_index] + str(octave)
    
    def highlight_note(self,note, action, velocity):
        if note in self.note_buttons:
            button = self.note_buttons[note]
            note_name = self.get_note_name(note)
            if "#" in note_name:
                if velocity == 64:
                    button.md_bg_color = (0.25,0.25,0.25,1) # Red
                    #button.style = "filled"
                else:
                    button.md_bg_color = (0,0,0,1) # Red
                    #button.style = "filled"

            else:
                if velocity == 64:

                    button.md_bg_color = (0.9,0.9,0.9,1)
                    #button.style = "elevated"
                else:
                    button.md_bg_color = (1,1,1,1)