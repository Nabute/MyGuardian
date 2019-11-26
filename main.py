from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics
from keras.utils import to_categorical, np_utils
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from datetime import datetime
import pandas as pd
import numpy as np
import librosa
import librosa.display
from tqdm import tqdm
import matplotlib.pyplot as plt
import IPython.display as ipd

import os



#file path for full data
dataPath = './voiceData/'
num_rows = 40
num_columns = 84
num_channels = 1
filterSize = 2

def wav2mfcc(filename):
#    maxPadLen = 84
    try:
        audio, sr = librosa.load(filename, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfccsScaled = np.mean(mfccs.T, axis=0)
#        pad_width = maxPadLen - mfccs.shape[1]
#        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        
    except Exception as e:
        print("Can't load file: ", filename)
        return None
    return mfccsScaled

def getLabels(path=dataPath):
    labels = os.listdir(path)
    label_indices = np.arange(0, len(labels))
    return labels, label_indices, to_categorical(label_indices)

# Preprocess every data

def preprocessVoiceData():
    features = []
    
    labels,_,_ = getLabels()
    for label in labels:
        filePath = os.path.join(dataPath, label)
        voiceFiles =[filePath + '/' + voice for voice in os.listdir(filePath)]
        for voice in tqdm(voiceFiles, "Extracting Features of {} voice Data".format(label)):
            data = wav2mfcc(voice)
            features.append([data, label])
    # creating dataframes
    df = pd.DataFrame(features, columns=['Feature', 'Label'])
    
    print('Finished Extraction completed from '+ str(len(df)) + ' files')
    
    # converting data and label into a numpy array
    x = np.array(df.Feature.tolist())
    
    y = np.array(df.Label.tolist())
    
    # Splitting dataset into training and testing data(s)
    _labelEncoder = LabelEncoder()
    _y = to_categorical(_labelEncoder.fit_transform(y))
    
    x_train, x_test, y_train, y_test = train_test_split(x, _y, test_size=0.2, random_state = 42) 
    
    # return the splitted data and fitted label encoder
    return x_train, x_test, y_train, y_test, _labelEncoder
        
def trainWithMLP():
    
    '''
    Using multilevel perseptron Neural Network.
    '''
    
    numEpochs = 100
    numBatchSize = 32
    outputFile= './outputs/out1.h5'
    
    x_train, x_test, y_train, y_test, labelEncoder = preprocessVoiceData()
    labels,_,_ = getLabels()
    numLabels = len(labels)
    
    # Creating model [nueral netword]
    model = Sequential()
    
#    Input layer
    model.add(Dense(256, input_shape=(40,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
#    Hidden Layer
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
#    Output Layer
    
    model.add(Dense(numLabels))
    model.add(Activation('softmax'))
    
#    compiling the model
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
    
    model.summary()
    
    # Calculate pre-training accuracy 
    # preScore = model.evaluate(x_test, y_test, verbose=1)
    # accuracy = 100*preScore[1]

    # print("Pre-training accuracy: %.4f%%" % accuracy)
    
    checkpointer = ModelCheckpoint(filepath='./models/weights.best.basic_mlp.hdf5', 
                               verbose=1, save_best_only=True)
    start = datetime.now()

    model.fit(x_train, y_train, batch_size=numBatchSize, epochs=numEpochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)
    
    # duration = datetime.now() - start
    # print("Training completed in time: ", duration)
    
#    Model evaluation
    testScore = model.evaluate(x_test, y_test, verbose=0)
    accuracy = 100*testScore[1]

    print("Accuracy of Test Data:= %.2f%%" % accuracy)
    
    trainScore = model.evaluate(x_train, y_train, verbose=0)
    accuracy = 100*trainScore[1]

    print("Accuracy of Training Data:= %.2f%%" % accuracy)
    
    validate(model, labelEncoder)
    
    print("Saving model to {}...".format(outputFile))
    model.save(outputFile)
    

def validate(model, labelEncoder):
    
    voiceFile = "./validations/recording.wav"
#    voiceFile = dataPath + "bad/" + "140853_SOUNDDOGS__sc.wav"
    
    sampleBadVoice = np.array([wav2mfcc(voiceFile)]) 
#    sampleGoodVoice = np.array([wav2mfcc(dataPath+ "good/" + "309972_SOUNDDOGS__ba.wav")])
    sampleGoodVoice = np.array([wav2mfcc(voiceFile)])
        
    print("-------------  VALIDATION  ----------------")
    displayVoiceData(voiceFile)
    
    bad_predicted_vector = model.predict_classes(sampleBadVoice)
    bad_predicted_class = labelEncoder.inverse_transform(bad_predicted_vector) 
    print("The predicted class for BAD voice sample data is:= ", bad_predicted_class[0], '\n') 
    
    good_predicted_vector = model.predict_classes(sampleGoodVoice)
    good_predicted_class = labelEncoder.inverse_transform(good_predicted_vector) 
    print("The predicted class for GOOD voice sample data is:= ", good_predicted_class[0], '\n') 
    

def displayVoiceData(filename):
    plt.figure(figsize=(12,4))
    data,sample_rate = librosa.load(filename)
    print("Data:= ")
    print(data)
    print("Sample Rate:= ")
    print(sample_rate)
    _ = librosa.display.waveplot(data,sr=sample_rate)
    ipd.Audio(filename)
    

def trainWithCNN():
    #TODO: To be implemented for the sake of Accuracy improvement
    # Using Convolutional Neural Network


if __name__ == "__main__":
    
    trainWithMLP()
#    trainWithCNN()