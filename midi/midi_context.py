import random
import subprocess
import time

from midi.data import sendmidi, scales, midi_note_values, Note


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

    def notes_in_scale(self, note_value=None, scale='major'):
        try:
            steps = scales[scale]
        except KeyError:
            print('"{}" is not a valid scale'.format(scale))
            raise

        root_note = note_value % 12
        step_additions = [sum(steps[:s[0] + 1]) for s in enumerate(steps)]
        # get first 11 notes in scale (the 12th will be repeat values)
        first_octave = [root_note + s for s in step_additions][:-1]
        all_octaves = [
            list(range(n, 128, 12)) for n in first_octave]

        # return list of all notes, sorted and flattened
        return sorted([y for x in all_octaves for y in x])

    def notes_in_octave_range(self, note_value=None, num_octaves=1):
        if not num_octaves:
            raise Exception('num_octaves cannot be {}'.format(num_octaves))

        distance = num_octaves * 12 + note_value
        midi_range_start = midi_note_values[0]
        midi_range_end = midi_note_values[-1]

        if num_octaves < 0:
            start = max(midi_range_start, distance)
            end = note_value
        else:
            start = note_value
            end = min(midi_range_end, distance)

        return list(range(start, end + 1))

    def scale_notes_in_range(self, note_value=None,
                             scale='major', notes_in_range=None):
        scale_notes = self.notes_in_scale(note_value=note_value, scale=scale)

        return [n for n in notes_in_range if n in scale_notes]

    def play_sequence(self, root_note=None, duration=0,
                      num_octaves=1, scale=None, randomize=False):
        note_value = root_note.number
        notes = self.notes_in_octave_range(
            note_value=note_value, num_octaves=num_octaves)

        if scale:
            notes = self.scale_notes_in_range(
                note_value=note_value, scale=scale, notes_in_range=notes)

        if randomize:
            random.shuffle(notes)

        for note in notes:
            self.pluck_note(Note(number=note, velocity=127), duration)

    def all_off(self):
        return self._send_midi_message(sendmidi['all_off'])
