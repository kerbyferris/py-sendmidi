from collections import namedtuple

"""
Syntax look up dictionary for the sendmidi cli
(https://github.com/gbevin/SendMIDI)
"""
sendmidi = dict(
    base_cmd='sendmidi',
    device='dev',
    note_on='on',
    note_off='off',
    all_off='panic',
)

# Note datatype
Note = namedtuple('Note', 'number velocity')

# All available MIDI note values
midi_note_values = range(128)

# Supported scales, reprented by step notation
scales = {
    'major': [0, 2, 2, 1, 2, 2, 2, 1],
    'minor': [0, 2, 1, 2, 2, 1, 2, 2],
    'dorian': [0, 2, 1, 2, 2, 2, 1, 2],
    'mixolydian': [0, 2, 2, 1, 2, 2, 1, 2],
}
