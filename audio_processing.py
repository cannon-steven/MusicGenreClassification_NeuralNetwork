import librosa
import numpy as np
import os
import csv
import librosa.feature
import librosa.display


# Change this variable once the model is trained
# to capture the single file audio inputs
model_trained = False
number_header_cols = 0


def make_dataset(header):
    '''
    Takes the header values that will be in the data.csv file.
    Opens a new file and populates the header and the rows using
    the generes (GTZAN) dataset via librosa.
    '''
    # open the file and write the first row with the header attributes
    file = open('data.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(header)
    # These are the genres in the GTZAN directories
    # and we are going to loop through those directories to get the wav files.
    genres = "blues classical country disco hiphop jazz metal pop reggae rock"
    for g in genres.split():
        # loop through the genres directory
        # and pick the wav file from each genre directory
        for filename in os.listdir(f'./genres/{g}'):
            # songname is the .wav filename
            songname = f'./genres/{g}/{filename}'
            #  sr = sampling rate, y = audio time series
            y, sr = librosa.load(songname, mono=True, duration=3)
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
            # take the mean of each parameter (except filename)
            # and append it as a string
            # tempo
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo = librosa.beat.tempo(y=y, sr=sr, onset_envelope=onset_env)
            # harmonics and percussiveness
            harmony, percussion = librosa.effects.hpss(y=y)
            to_append = f'''{filename} {np.mean(chroma_stft)}\
                        {np.var(chroma_stft)} {np.mean(rms)}\
                        {np.var(rms)} {np.mean(spec_cent)}\
                        {np.var(spec_cent)} {np.mean(spec_bw)}\
                        {np.var(spec_bw)} {np.mean(rolloff)}\
                        {np.var(rolloff)} {np.mean(zcr)} {np.var(zcr)}\
                        {np.mean(harmony)} {np.var(harmony)}\
                        {np.mean(percussion)} {np.var(percussion)}
                        {np.sum(tempo)}'''
            # loop through all the mfcc values and append them
            # together to add them on the to_append variable
            for e in mfcc:
                to_append += f' {np.mean(e)} {np.var(e)}'
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
    header = '''filename chroma_stft_mean chroma_stft_var rms_mean rms_var
    spectral_centroid_mean spectral_centroid_var
    spectral_bandwidth_mean spectral_bandwidth_var
    rolloff_mean rolloff_var zero_crossing_rate_mean
    zero_crossing_rate_var harmony_mean
    harmony_var perceptr_mean perceptr_var tempo mfcc1_mean
    mfcc1_var mfcc2_mean mfcc2_var
    mfcc3_mean mfcc3_var mfcc4_mean mfcc4_var mfcc5_mean
    mfcc5_var mfcc6_mean mfcc6_var
    mfcc7_mean mfcc7_var mfcc8_mean mfcc8_var mfcc9_mean
    mfcc9_var mfcc10_mean mfcc10_var
    mfcc11_mean mfcc11_var mfcc12_mean mfcc12_var
    mfcc13_mean mfcc13_var mfcc14_mean mfcc14_var
    mfcc15_mean mfcc15_var mfcc16_mean mfcc16_var
    mfcc17_mean mfcc17_var mfcc18_mean mfcc18_var
    mfcc19_mean mfcc19_var mfcc20_mean mfcc20_var'''
    header = header.split()
    # Make sure the length of the headers is correct
    make_dataset(header)


if __name__ == '__main__':
    init_dataset_header()
