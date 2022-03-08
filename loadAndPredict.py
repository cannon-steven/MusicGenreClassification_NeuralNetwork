import tensorflow as tf
import keras.models
import matplotlib.pyplot as plt
import numpy as np
import os
import librosa
import librosa.display


imageHeight = 369
imageWidth = 496


class_names = ['blues', 'classical', 'country', 'hiphop', 'jazz', 'pop',
               'metal', 'reggae', 'rock']



def makePrediction(song):
    model = keras.models.load_model("MusicClassifier")

    # Load song from the middle point and only use 3 seconds
    y_forLength, sr = librosa.load(song)
    songLength = librosa.get_duration(y=y_forLength, sr=sr)
    midpoint = songLength // 2


    #########################################################################

    # To load entire song ###################################################

    # y, sr = librosa.load(song)

    #########################################################################

    # To load first 30 seconds of song ######################################

    # y, sr = librosa.load(song, duration=30)


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
    img_array = tf.keras.utils.load_img(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Send spectrogram to model to make prediction
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Remove temp file
    os.remove('tempSpec.png')

    return np.array(score)
