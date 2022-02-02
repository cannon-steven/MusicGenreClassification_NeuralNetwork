import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import librosa.feature
# Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
#Keras
import keras

def make_dataset(header):
    '''
    Takes the header values that will be in the data.csv file.
    Opens a new file and populates the header and the rows using the generes (GTZAN) dataset via librosa.
    '''
    # open the file and write the first row with the header attributes
    file = open('data.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    # These are the genres in the GTZAN directories and we are going to loop through those directories to get the wav files.
    genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()
    for g in genres:
        # loop through the genres directory and pick the wav file from each genre directory
        for filename in os.listdir(f'./genres/{g}'):
            # songname is the .wav filename
            songname = f'./genres/{g}/{filename}'
            #  sr = sampling rate, y = audio time series
            y, sr = librosa.load(songname, mono=True, duration=30)
            # chroma short time fourier transform
            chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
            # root mean square deviation
            rmse = librosa.feature.rmse(y=y)
            # spectral centroid
            spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            # spectral bandwidth
            spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
            # spectral rolloff
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            # zero crossing rate 
            zcr = librosa.feature.zero_crossing_rate(y)
            # The Mel-Frequency Cepstral Coefficients (21 in our case)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            # take the mean of each attribute and append it as a string
            to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'    
            # loop through all the mfcc values and append them together to add them on the to_append variable
            for e in mfcc:
                to_append += f' {np.mean(e)}'
            to_append += f' {g}'
            # add the row of attributes into our data.csv file
            file = open('data.csv', 'a', newline='')
            with file:
                writer = csv.writer(file)
                writer.writerow(to_append.split())
            


def init_dataset_header():
    '''
    Initializes the header for the data.csv file.
    Uses the make_dataset() function to generate the data.csv file. 
    '''
    header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
    
    # I need to generate 21 columns in the csv file for the mfcc values
    for i in range(1, 21):
        header += f' mfcc{i}'
    header += ' label'
    header = header.split()
    # Use the function and pass it the header
    make_dataset(header)
    
    
if __name__=='__main__':
    init_dataset_header()
    