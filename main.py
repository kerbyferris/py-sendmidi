from midi.midi_context import MidiContext
from midi.data import Note

if __name__ == '__main__':

    ctx = MidiContext('UM-ONE')
    note = Note(number='c2', velocity=127)
    ctx.pluck_note(note)
    ctx.all_off()
