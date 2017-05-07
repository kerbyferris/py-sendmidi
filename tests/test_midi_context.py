import pytest
from unittest.mock import MagicMock, patch

from faker import Faker

from midi.midi_context import MidiContext
from midi.data import Note, sendmidi


@pytest.fixture()
def midi_ctx():
    device = 'test_device'
    ctx = MidiContext(device)

    return ctx


@pytest.fixture()
def note():
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
