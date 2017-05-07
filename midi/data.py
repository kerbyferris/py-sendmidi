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

# Declare Note datatype
Note = namedtuple('Note', 'number velocity')
