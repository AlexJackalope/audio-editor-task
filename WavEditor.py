import os
import sys
import wave
from pysndfx import AudioEffectsChain


class WavEditor():
    def __init__(self, audio_path):
        self.channels = None
        self.sample_width = None
        self.rate = None
        self.signal = None
        self.pre_previous_state = None
        self.previous_state = None
        self.state_index = 0
        self.clear_states(exception=os.path.split(audio_path)[1])
        self.current_state = audio_path
        self.setup_current_characteristics()

    def setup_current_characteristics(self):
        try:
            with wave.open(self.current_state, 'rb') as audio:
                self.channels = audio.getnchannels()
                self.sample_width = audio.getsampwidth()
                self.rate = audio.getframerate()
                self.signal = audio.readframes(-1)
        except wave.Error as e:
            print("File cannot be converted to a supported format" + e.args[0])
            sys.exit()

    def clear_states(self, exception=None):
        dir_path = os.path.join(os.path.dirname(__file__), 'EditorFiles')
        for file_object in os.listdir(dir_path):
            if file_object == exception:
                continue
            os.remove(os.path.join(dir_path, file_object))
        self.pre_previous_state = None
        self.previous_state = None
        self.current_state = None

    def shift_states(self):
        if self.pre_previous_state is not None:
            os.remove(self.pre_previous_state)
        self.pre_previous_state, self.previous_state = \
            self.previous_state, self.current_state
        self.current_state = self.new_state
        if self.state_index < 4:
            self.state_index += 1
        else:
            self.state_index = 0

    def rollback(self):
        if self.previous_state is not None:
            self.current_state, self.previous_state = \
                self.previous_state, self.pre_previous_state
            self.pre_previous_state = None
            self.setup_current_characteristics()
        else:
            raise RuntimeError("Nowhere to rollback")

    def create_new_state(self):
        filename = 'editedAudioData' + str(self.state_index) + '.wav'
        self.new_state = os.path.join(os.path.dirname(__file__),
                                      'EditorFiles', filename)
        with open(self.new_state, 'w'):
            pass

    def fill_new_state(self):
        self.create_new_state()
        with wave.open(self.new_state, 'wb') as result:
            result.setnchannels(self.channels)
            result.setsampwidth(self.sample_width)
            result.setframerate(self.rate)
            result.writeframes(self.signal)
        self.shift_states()

    def speed_chg(self, coefficient):
        self.rate *= coefficient
        self.fill_new_state()
        print('Speed changing complited')

    def cut(self, start, length):
        start = int(start)
        length = int(length)
        per_second = self.sample_width * self.rate * self.channels
        start_byte = start * per_second
        if start_byte >= len(self.signal):
            raise AttributeError('Your audio is only ' +
                                 str(len(self.signal) // per_second) +
                                 'seconds long')
        end_byte = start_byte + length * per_second
        self.signal = self.signal[start_byte:end_byte]
        self.fill_new_state()
        print('Cutting complited')

    def concat(self, new_file):
        with wave.open(new_file, 'rb') as audio:
            channels = audio.getnchannels()
            sample_width = audio.getsampwidth()
            rate = audio.getframerate()
            signal = audio.readframes(-1)
        if channels != self.channels \
                or sample_width != self.sample_width \
                or rate != self.rate:
            print("Sorry, these audios are incompatible")
            return
        self.signal = self.signal + signal
        self.fill_new_state()
        print('Concatination complited')

    def reverb(self, size):
        size = int(size)
        if size < 0 or size > 100:
            print('Reverberation room scale must be between 0 and 100')
            return
        fx = (AudioEffectsChain().reverb(room_scale=size))
        self.create_new_state()
        fx(self.current_state, self.new_state)
        self.shift_states()
        print('Reverberation complited')

    def normalize(self):
        fx = (AudioEffectsChain().normalize())
        self.create_new_state()
        fx(self.current_state, self.new_state)
        self.shift_states()
        print('Normalization complited')
