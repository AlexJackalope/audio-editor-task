import os
import sys
import wave
from unittest import TestCase
from WavEditor import WavEditor
from WavConverter import WavConverter

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))


class TestsWavEditor(TestCase):
    def setUp(self) -> None:
        self.wav_path = os.path.join(os.path.dirname(__file__), 'Fox.wav')
        self.editor = WavEditor(self.wav_path)

    def test_speed_up(self):
        self.editor.speed_chg(1.5)
        with wave.open(self.wav_path) as sourse:
            prev_rate = sourse.getframerate()
        with wave.open(self.editor.current_state) as edited:
            rate = edited.getframerate()
        assert rate == 1.5 * prev_rate

    def test_cut(self):
        self.editor.cut(2, 5)
        with wave.open(self.editor.current_state) as edited:
            channels = edited.getnchannels()
            sample_width = edited.getsampwidth()
            rate = edited.getframerate()
            content = edited.readframes(-1)
        assert len(content) == channels * sample_width * rate * 5

    def test_cut_out_of_bounds(self):
        with self.assertRaises(AttributeError):
            self.editor.cut(20, 20)

    def tearDown(self) -> None:
        self.editor.clear_states()


class TestsConverter(TestCase):
    def setUp(self) -> None:
        self.wav_path = os.path.join(os.path.dirname(__file__), 'Fox.wav')
        self.converter = WavConverter()
        self.converter = WavConverter()

    def test_filechecks(self):
        self.converter.check_file(self.wav_path)
        with self.assertRaises(FileNotFoundError):
            self.converter.check_file('notexisting')
        with self.assertRaises(NameError):
            self.converter.check_file('tests.py')
