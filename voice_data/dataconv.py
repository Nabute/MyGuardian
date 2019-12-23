import librosa as lb
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('~/Documents/GitHub/MyGuardian/voice_data/Babies data/')

#457 files 

class dataConv:
    def __init__(self):
        self.val = 0
        self.voice = [[]]
        self.counter = 0

    def main(self):
        for i in self.pathtolist():
            voicepath = "voice_data/Babies data/negative/" + i
            data, fs = lb.load(voicepath)
            print(voicepath, "  ", self.counter)
            data = np.asarray(data)
            self.appendValue(data)
            self.counter += 1
            if self.counter == 1000:
                break 
        self.saveFile()

    def appendValue(self, val):
        self.voice.append(val)

    def pathtolist(self):
        return os.listdir(path='voice_data/Babies data/negative/')

    def saveFile(self):
        self.voice = np.asarray(self.voice)
        np.save("voice_data/negative-voices.npy", self.voice)

    def drawVoice(self, ardata):
        plt.plot(ardata)
        plt.ylabel('voice data')
        plt.show()



if __name__=='__main__':
    obj = dataConv()
    obj.main()