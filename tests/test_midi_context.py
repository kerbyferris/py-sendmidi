from unittest.mock import MagicMock, patch

from faker import Faker
import pytest

from midi.midi_context import MidiContext
from midi.data import Note, sendmidi


@pytest.fixture()
def midi_ctx():
    device = 'test_device'
    ctx = MidiContext(device)

    return ctx


@pytest.fixture()
def note():
    # middle C at full volume
    note_value = 60
    velocity = 127

    return Note(number=note_value, velocity=velocity)


class TestMidiContext():
    fake = Faker()

    @patch('subprocess.run', return_value=None)
    def test_send_midi_message(self, mock_run, midi_ctx):
        cmd = self.fake.sentence(nb_words=3)
        midi_ctx._send_midi_message(cmd)

        mock_run.assert_called_with(
            ' '.join([midi_ctx.cmd_prefix, cmd]),
            shell=True
        )

    def test_build_note_message(self, midi_ctx, note):
        state = self.fake.word()

        midi_ctx._send_midi_message = MagicMock(return_value=True)
        midi_ctx._build_note_message(state, note)

        midi_ctx._send_midi_message.assert_called_with(
            '{} {} {}'.format(state, note.number, note.velocity))

    def test_start_note(self, midi_ctx, note):
        midi_ctx._build_note_message = MagicMock(return_value=True)

        midi_ctx.start_note(note)

        midi_ctx._build_note_message.assert_called_with(
            state=sendmidi['note_on'], note=note)

    def test_stop_note(self, midi_ctx, note):
        midi_ctx._build_note_message = MagicMock(return_value=True)

        midi_ctx.stop_note(note)

        midi_ctx._build_note_message.assert_called_with(
            state=sendmidi['note_off'], note=note)

    @patch('time.sleep', return_value=None)
    def test_pluck_note(self, mock_sleep, midi_ctx, note):
        midi_ctx.start_note = MagicMock(return_value=True)
        midi_ctx.stop_note = MagicMock(return_value=True)

        duration = self.fake.random_int()

        midi_ctx.pluck_note(note, duration)

        midi_ctx.start_note.assert_called_with(note)
        mock_sleep.assert_called_with(duration)
        midi_ctx.stop_note.assert_called_with(note)

    def test_all_off(self, midi_ctx):
        midi_ctx._send_midi_message = MagicMock(return_value=True)

        midi_ctx.all_off()

        midi_ctx._send_midi_message.assert_called_with(sendmidi['all_off'])

    def test_notes_in_scale(self, midi_ctx, note):
        middle_c = note.number
        # notes in scales based on middle c as root
        major = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26, 28,
                 29, 31, 33, 35, 36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53,
                 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79,
                 81, 83, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100, 101, 103,
                 105, 107, 108, 110, 112, 113, 115, 117, 119, 120, 122, 124,
                 125, 127]
        # single octave examples
        minor = [60, 62, 63, 65, 67, 68, 70, 72]
        dorian = [60, 62, 63, 65, 67, 69, 70, 72]
        mixolydian = [60, 62, 64, 65, 67, 69, 70, 72]

        with pytest.raises(Exception):
            (midi_ctx.notes_in_scale(
                note_value=middle_c, scale='not_a_valid_scale'))

        assert(midi_ctx.notes_in_scale(
            note_value=middle_c, scale='major') == major)
        assert(all([m in midi_ctx.notes_in_scale(
            note_value=middle_c, scale='minor') for m in minor]))
        assert(all([m in midi_ctx.notes_in_scale(
            note_value=middle_c, scale='dorian') for m in dorian]))
        assert(all([m in midi_ctx.notes_in_scale(
            note_value=middle_c, scale='mixolydian') for m in mixolydian]))

    def test_notes_in_octave_name(self, midi_ctx, note):
        middle_c = note.number

        assert(midi_ctx.notes_in_octave_range(
            note_value=middle_c, num_octaves=2) == list(range(60, 85)))
        assert(midi_ctx.notes_in_octave_range(
            note_value=middle_c, num_octaves=-2) == list(range(36, 61)))
        assert(midi_ctx.notes_in_octave_range(
            note_value=middle_c, num_octaves=-6) == list(range(61)))
        assert(midi_ctx.notes_in_octave_range(
            note_value=middle_c, num_octaves=6) == list(range(60, 128)))
        with pytest.raises(Exception):
            (midi_ctx.notes_in_octave_range(
                note_value=middle_c, num_octaves=0))
        with pytest.raises(Exception):
            (midi_ctx.notes_in_octave_range(
                note_value=middle_c, num_octaves=None))

    def test_scale_notes_in_range(self, midi_ctx, note):
        middle_c = note.number
        test_range = list(range(8))

        assert(midi_ctx.scale_notes_in_range(
            note_value=middle_c,
            notes_in_range=test_range) == [0, 2, 4, 5, 7])
        assert(midi_ctx.scale_notes_in_range(
            note_value=middle_c,
            notes_in_range=test_range, scale='minor') == [0, 2, 3, 5, 7])

    @patch('random.shuffle', return_value=None)
    def test_play_sequence(self, mock_shuffle, midi_ctx, note):
        middle_c = note.number
        middle_c_major_notes = [
            60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]

        last_note_in_seq = Note(number=72, velocity=127)
        midi_ctx.pluck_note = MagicMock(return_value=True)
        midi_ctx.scale_notes_in_range = MagicMock(
            return_value=[middle_c_major_notes])

        midi_ctx.play_sequence(root_note=note, duration=1)

        midi_ctx.pluck_note.assert_called_with(last_note_in_seq, 1)
        mock_shuffle.assert_not_called

        midi_ctx.play_sequence(root_note=note, scale='major')
        midi_ctx.scale_notes_in_range.assert_called_with(
            note_value=middle_c, notes_in_range=middle_c_major_notes,
            scale='major')

        midi_ctx.play_sequence(root_note=note, randomize=True)
        mock_shuffle.assert_called_with(middle_c_major_notes)
