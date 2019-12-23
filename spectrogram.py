import wave
import pylab
import os

class spectrogram:
    def __init__(self, filepath):
        self.path = filepath
        assert filepath in os.listdir(path='.'), "File not found, Please specify a correct path for your .wav file"
    
    def graph_spectrogram(self, save=False):
        sound_info, frame_rate = self.get_wav_info()
        pylab.figure(num=None, figsize=(19, 12))
        pylab.subplot(111)
        pylab.title('spectrogram of %r' % self.path)
        pylab.specgram(sound_info, Fs=frame_rate)
        pylab.show()

        if save:
            pylab.savefig('spectrogram.png')

    def get_wav_info(self):
        wav = wave.open(self.path, 'r')
        frames = wav.readframes(-1)
        sound_info = pylab.frombuffer(frames, 'int16')
        frame_rate = wav.getframerate()
        wav.close()
        return sound_info, frame_rate


if __name__ == '__main__':
    sp = spectrogram('spectrogrm-1.wav')
    sp.graph_spectrogram()
