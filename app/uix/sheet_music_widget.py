from kivy.uix.widget import Widget
import mingus.core.notes as notes
import sys
sys.path.append('./app/')
from core.midi_handler import start_music


class SheetMusicWidget(Widget):
    start_music()
