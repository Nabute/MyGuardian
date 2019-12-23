import librosa as lb
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('~/Documents/GitHub/MyGuardian/voice_data/Babies data/')



data = np.load("voice_data/babyvoice-positive.npy", allow_pickle=True)

data = np.asarray(data[50])
print(data)
plt.plot(data)
plt.ylabel('voice data')
plt.show()