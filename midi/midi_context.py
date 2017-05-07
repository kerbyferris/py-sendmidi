import subprocess
import time
from midi.data import sendmidi


class MidiContext():

    def __init__(self, device):
        self.cmd_base = ' '.join([sendmidi['base_cmd'], sendmidi['device']])
        self.device = device
        self.cmd_prefix = ' '.join([self.cmd_base, self.device])

    def _send_midi_message(self, cmd):
        subprocess.run(' '.join([self.cmd_prefix, cmd]), shell=True)

    def _build_note_message(self, state=None, note=None):
        cmd = '{} {} {}'.format(state, note.number, note.velocity)
        self._send_midi_message(cmd)

    def start_note(self, note):
        self._build_note_message(state=sendmidi['note_on'], note=note)

    def stop_note(self, note):
        self._build_note_message(state=sendmidi['note_off'], note=note)

    def pluck_note(self, note, duration=0):
        self.start_note(note)
        time.sleep(duration)
        self.stop_note(note)

    def all_off(self):
        return self._send_midi_message(sendmidi['all_off'])
