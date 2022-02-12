from tensorflow import keras
import csv
import numpy as np
import pandas as pd
import os
import librosa

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

# SONG_PATH = "Clincher.wav"
# SONG_PATH = "Pathfinder.wav"
# SONG_PATH = "someOtherMetal.wav"
# SONG_PATH = "Metal3.wav"
SONG_PATH = "California.wav"
# SONG_PATH = "Father.wav"


def make_dataset(header, songFile):
    """
    Takes the header values that will be in the data.csv file.
    Opens a new file and populates the header and the rows using
    the generes (GTZAN) dataset via librosa.
    """
    # open the file and write the first row with the header attributes
    file = open('testData.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)

    #  sr = sampling rate, y = audio time series
    y, sr = librosa.load(songFile, mono=True, duration=30)
    # chroma short time fourier transform
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    # root mean square deviation
    rms = librosa.feature.rms(y=y)
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
    # harmonics and percussiveness
    harmony, percussion = librosa.effects.hpss(y=y)
    # tempo
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.beat.tempo(y=y, sr=sr, onset_envelope=onset_env)
    # take the mean of each parameter (except filename)
    # and append it as a string
    to_append = f'{np.mean(chroma_stft)} {np.var(chroma_stft)} {np.mean(rms)} {np.var(rms)} {np.mean(spec_cent)}'\
                + f'{np.var(spec_cent)} {np.mean(spec_bw)} {np.var(spec_bw)} {np.mean(rolloff)} {np.var(rolloff)}'\
                + f'{np.mean(zcr)} {np.var(zcr)} {np.mean(harmony)} {np.var(harmony)} {np.mean(percussion)}'\
                + f'{np.var(percussion)} {np.sum(tempo)}'

    # loop through all the mfcc values and append them
    # together to add them on the to_append variable
    for e in mfcc:
        to_append += f' {np.mean(e)} {np.var(e)}'

    # add the row of attributes into our data.csv file
    file = open('testData.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(to_append.split())


def init_dataset_header():
    """
    Initializes the header for the data.csv file.
    Uses the make_dataset() function to generate the data.csv file.
    """
    header = '''chroma_stft_mean chroma_stft_var rms_mean rms_var 
    spectral_centroid_mean spectral_centroid_var spectral_bandwidth_mean spectral_bandwidth_var 
    rolloff_mean rolloff_var zero_crossing_rate_mean zero_crossing_rate_var harmony_mean 
    harmony_var perceptr_mean perceptr_var tempo mfcc1_mean mfcc1_var mfcc2_mean mfcc2_var 
    mfcc3_mean mfcc3_var mfcc4_mean mfcc4_var mfcc5_mean mfcc5_var mfcc6_mean mfcc6_var 
    mfcc7_mean mfcc7_var mfcc8_mean mfcc8_var mfcc9_mean mfcc9_var mfcc10_mean mfcc10_var 
    mfcc11_mean mfcc11_var mfcc12_mean mfcc12_var mfcc13_mean mfcc13_var mfcc14_mean mfcc14_var 
    mfcc15_mean mfcc15_var mfcc16_mean mfcc16_var mfcc17_mean mfcc17_var mfcc18_mean mfcc18_var 
    mfcc19_mean mfcc19_var mfcc20_mean mfcc20_var'''
    header = header.split()
    # Use the function and pass it the header
    # make_dataset(header)
    return header


def predict(model, file):
    header = init_dataset_header()
    make_dataset(header, file)
    df = pd.read_csv("testData.csv")

    # perform prediction
    prediction = model.predict(df)

    # get index with max value
    predicted_index = np.argmax(prediction, axis=1)

    predicted_genre = indexToGenre(predicted_index)

    return predicted_genre


def indexToGenre(param):
    if 0 <= param <= 9:
        genres = ["Blues", "Classical", "Country", "Disco", "Hiphop", "Jazz", "Metal", "Pop", "Reggae", "Rock"]
        return genres[param]
    else:
        return "Error"


if __name__ == '__main__':
    header = init_dataset_header()
    make_dataset(header, SONG_PATH)
    model = keras.models.load_model("my_model")
    print(predict(model))
