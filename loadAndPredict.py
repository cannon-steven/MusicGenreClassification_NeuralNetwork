import tensorflow as tf
import keras.models
import matplotlib.pyplot as plt
import numpy as np
import os
import librosa
import librosa.display
from pydub import AudioSegment
import matplotlib
matplotlib.use('Agg')

imageHeight = 369
imageWidth = 496

class_names = ['blues', 'classical', 'country', 'hiphop', 'jazz', 'pop',
               'metal', 'reggae', 'rock']


def mp3_to_wav(mp3FilePath):
    """
    Given the path to an .mp3 file, creates a .wav copy and returns the path to
    the copy
    """
    # Get file path as .wav
    wavFilePath = f"{mp3FilePath[0:-4]}.wav"

    # Copy mp3 file to wav
    sound = AudioSegment.from_mp3(mp3FilePath)
    sound.export(wavFilePath, format="wav")

    return wavFilePath


def makePrediction(song, mp3=True):
    """
    Given the path to a .wav file, makes a prediction on the genre of the song.
    Returns an array of confidences for the 10 genres
    """
    model = keras.models.load_model("MusicClassifier")

    if mp3:
        song = mp3_to_wav(song)

    # Load song from the middle point and only use 3 seconds
    y_forLength, sr = librosa.load(song)
    songLength = librosa.get_duration(y=y_forLength, sr=sr)
    midpoint = songLength // 2

    # Get clip as spectrogram
    y, sr = librosa.load(song, offset=midpoint, duration=3)
    plt.axis("off")  # Needed to remove white border from saved image.
    data = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(data), ref=np.max)
    librosa.display.specshow(S_db)

    # Save file to temp
    tempfile = "tempSpec.png"
    plt.savefig(
        tempfile,
        bbox_inches="tight",  # This and pad_inches and plt.axis("off") remove
        pad_inches=0.0        # the white borders from the image
    )

    # Load spectrogram
    img = tf.keras.utils.load_img(tempfile, target_size=(imageHeight,
                                  imageWidth))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Send spectrogram to model to make prediction
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Remove temp file
    os.remove('tempSpec.png')

    return np.array(score)
