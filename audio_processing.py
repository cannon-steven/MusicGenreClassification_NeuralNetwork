import librosa
import numpy as np
import os
import csv
import librosa.feature
import librosa.display
import matplotlib.pyplot as plt
# Change this variable once the model is trained
# to capture the single file audio inputs
model_trained = True
get_spectrogram = False


def get_spectrogram_from_input_file(songname):
    # Gets you a spectrogram of the input file by the user.
    audio_path = os.path.abspath(songname)
    x, sr = librosa.load(audio_path, sr=None)
    # display Spectrogram
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    # If to pring log of frequencies
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar()


def make_tuple(key, value):
    return (key, value)


def make_dictionary(array_tuples):
    return dict(array_tuples)


def get_data_array(song_name):

    arr = []
    # songname is the .wav filename
    songname = os.path.abspath(song_name)
    #  sr = sampling rate, y = audio time series
    y, sr = librosa.load(songname, mono=True, duration=30)
    # chroma short time fourier transform
    arr.append(make_tuple('chroma_stft',
                          np.mean(librosa.feature.chroma_stft(y=y, sr=sr))))
    # root mean square deviation
    arr.append(make_tuple('rmse', np.mean(librosa.feature.rmse(y=y))))
    # spectral centroid
    arr.append(make_tuple('spectral_c', np.mean(
        librosa.feature.spectral_centroid(y=y, sr=sr))))
    # spectral bandwidth
    arr.append(make_tuple('spectral_bw', np.mean(
                          librosa.feature.spectral_bandwidth(y=y, sr=sr))))
    # spectral rolloff
    arr.append(make_tuple('spectral_rf', np.mean(
                          librosa.feature.spectral_rolloff(y=y, sr=sr))))
    # zero crossing rate
    arr.append(make_tuple('zcr', np.mean(
                          librosa.feature.zero_crossing_rate(y))))
    # The Mel-Frequency Cepstral Coefficients (20 in our case)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    # loop through all the mfcc values and add them to an array
    index = 0
    for e in mfcc:
        index += 1
        arr.append(make_tuple(f"mfcc{index}", np.mean(e)))
    return arr


def get_wav_path(song_name):
    # songname is the .wav filename
    return os.path.abspath(song_name)


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
            # take the mean of each parameter (except filename)
            # and append it as a string
            to_append = f'{filename} {np.mean(chroma_stft)}'
            to_append = f'{np.mean(rmse)} {np.mean(spec_cent)}'
            to_append = f'{np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'

            # loop through all the mfcc values and append them
            # together to add them on the to_append variable
            for e in mfcc:
                to_append += f' {np.mean(e)}'
            to_append += f' {g}'
            # add the row of attributes into our data.csv file
            file = open('data.csv', 'a', newline='')
            with file:
                writer = csv.writer(file)
                writer.writerow(to_append.split())


def init_dataset_header(song_name):
    '''
    Initializes the header for the data.csv file.
    Uses the make_dataset() function to generate the data.csv file.
    '''
    header = '''filename chroma_stft rmse spectral_centroid
    spectral_bandwidth rolloff zero_crossing_rate'''

    # I need to generate 21 columns in the csv file for the mfcc values
    for i in range(1, 21):
        header += f' mfcc{i}'
    header += ' label'
    header = header.split()
    # Use the function and pass it the header
    if model_trained:
        # get the spectrogram of the song:
        # get_spectrogram_from_input_file()
        # populate the array with the values we want.
        # populate the dictionary with the key: value pairs we want
        array_tuples = get_data_array(song_name)
        # make sure that this is length 26
        new_dict_with_data = make_dictionary(array_tuples)
        # call this function and return the dictionary
        return new_dict_with_data
    else:
        # make the dataset
        make_dataset(header)


if __name__ == '__main__':
    print(init_dataset_header('song_name.wav'))
    if get_spectrogram:
        get_spectrogram_from_input_file('song_name.wav')
