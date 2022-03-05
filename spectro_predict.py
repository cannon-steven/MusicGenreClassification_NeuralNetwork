# This script has two exportable functions:
# predict_data() - for input of model and user spectrogram to get a prediction.
# new_spectrogram() - for generating a spectrogram from user .wav input.
import librosa.display
import librosa
import keras
import matplotlib.pyplot as plt
import os
import numpy as np
import tensorflow as tf
songname = 'pop_song.wav'

img_height = 400
img_width = 500

genre_names = ["Blues", "Classical", "Country", "Disco",
               "Hiphop", "Jazz", "Metal", "Pop", "Reggae", "Rock"]


def predict_data(model):
    random_spectro_file = "pop_song.wav.png"
    spectro_path = tf.keras.utils.get_file(
        'songname', origin=random_spectro_file)
    img = tf.keras.utils.load_img(
        spectro_path, target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    return score


def new_spectrogram(wav_file):
    # Gets you a spectrogram of the input file by the user.
    # Get filename
    spectro_file = os.path.abspath(wav_file)
    spectro_file += ".png"
    y, sr = librosa.load(wav_file, sr=None)
    data = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(data), ref=np.max)
    librosa.display.specshow(S_db)
    # Save file to destination
    plt.savefig(spectro_file)


if __name__ == '__main__':
    new_spectrogram(songname)
    model = keras.models.load_model("my_model")
    score = predict_data(model)
    print("""This image most likely belongs
          to {} with a {:.2f} percent confidence.""".format(
              genre_names[np.argmax(score)], 100 * np.max(score)))
