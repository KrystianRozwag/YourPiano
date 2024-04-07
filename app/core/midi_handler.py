from mido import MidiFile, MidiTrack
from kivymd.uix.button import MDButtonText
import time
from datetime import datetime
import mido
import threading
class MidiHandler:
    def __init__(self, note_buttons):
        self.recording = False
        self.inport = ""
        self.note_buttons = note_buttons
    def connect_device(self, connect_message, record_btn):
        for input in mido.get_input_names():
            if "Digital Piano" in input:
                self.inport = mido.open_input(input)
                connect_message.text = "Connection Success to " + str(self.inport)
                self.listener_thread = threading.Thread(target=self.midi_listener, daemon=True)
                self.listener_thread.start()
                record_btn.disabled = False
                return input
        connect_message.text = "Connection Failed"


    def toggle_recording(self, record_btn):
        if self.recording:
            self.stop_recording()
            now = datetime.now()
            dt_string =  now.strftime("%d-%m-%Y %H-%M-%S") + " - midi.mid"
            self.save_midi(dt_string)
            record_btn.add_widget(MDButtonText(text="Start Recording"))
        else:
            record_btn.add_widget(MDButtonText(text="Stop Recording"))
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

    def highlight_note(self,note, action, velocity):
        if note in self.note_buttons:
            button = self.note_buttons[note]
            if note % 2 != 0:
                if velocity == 64:
                    button.md_bg_color = (0.1,0.1,0.1,1) # Red
                    #button.style = "filled"
                else:
                    button.md_bg_color = (0,0,0,1) # Red
                    #button.style = "filled"

            elif note % 2 == 0:
                if velocity == 64:

                    button.md_bg_color = (0.9,0.9,0.9,1)
                    #button.style = "elevated"
                else:
                    button.md_bg_color = (1,1,1,1)