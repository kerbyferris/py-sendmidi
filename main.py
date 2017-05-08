from midi.midi_context import MidiContext
from midi.data import Note

if __name__ == '__main__':
    ctx = MidiContext('UM-ONE')
    root_note = Note(number=60, velocity=127)

    for _ in range(10):
        ctx.play_sequence(
            root_note=root_note, duration=.25, scale='dorian', randomize=True)

    ctx.all_off()
