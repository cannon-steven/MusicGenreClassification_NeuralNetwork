import tensorflow as tf
import keras.models
import matplotlib.pyplot as plt
import numpy as np
import os
import librosa
import librosa.display
from PIL import Image
import matplotlib
matplotlib.use('Agg')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

# local files on my computer for testing
# SONG_PATH = "Pathfinder.wav"
# SONG_PATH = "Clincher.wav"
# SONG_PATH = "California.wav"
# SONG_PATH = "Metal3.wav"
# SONG_PATH = "SomeOtherMetal.wav"
# SONG_PATH = "hiphop_song.wav"
# SONG_PATH = "Follow.wav"
# SONG_PATH = "hiphop.00000.wav"
# SONG_PATH = "pop.00000.wav"

imageHeight = 149
imageWidth = 200

class_names = ['blues', 'classical', 'country', 'hiphop', 'jazz', 'pop', 'metal', 'reggae', 'rock']


def makePrediction(song):
    model = keras.models.load_model("MusicClassifier")

    # To load song from the middle point and only use 3 seconds ############

    y_forLength, sr = librosa.load(song)
    songLength = librosa.get_duration(y=y_forLength, sr=sr)
    midpoint = songLength // 2
    y, sr = librosa.load(song, offset=midpoint, duration=6)

    #########################################################################

    # To load entire song ###################################################

    # y, sr = librosa.load(song)

    #########################################################################

    # To load first 30 seconds of song ######################################

    # y, sr = librosa.load(song, duration=30)

    #########################################################################

    plt.axis('off')  # no axis
    plt.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
    data = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(data), ref=np.max)
    librosa.display.specshow(S_db)
    plt.margins(0)

    plt.savefig("tempSpec.png")

    image = Image.open('tempSpec.png')
    image.thumbnail((200, 200))
    image.save('tempThumb.png')

    img = tf.keras.utils.load_img(
        'tempThumb.png', target_size=(imageHeight, imageWidth)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = img_array / 255
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # predictions = model.predict(img_array)
    predictions = model(img_array)
    score = tf.nn.softmax(predictions[0])
    # print(predictions)
    print(score)
    #
    # # norm = tf.keras.utils.normalize(predictions[0], axis=-1, order=2)
    #
    # # norm = np.array(norm)
    # print(norm)
    #
    # newNorm = []
    # for x in norm:
    #     y = x * 1000
    #     newNorm.append(y)
    #
    # # tf.math.round(newNorm)
    # print(newNorm)
    # score = tf.nn.softmax(newNorm)
    # print(score)

    os.remove('tempSpec.png')
    os.remove('tempThumb.png')

    return np.array(score)
    # print(
    #     "This image most likely belongs to {} with a {:.2f} percent confidence."
    #         .format(class_names[np.argmax(score)], 100 * np.max(score))
    # )

    # print(
    #     "This image most likely belongs to {} with a {:.2f} percent confidence."
    #     .format(class_names[np.argmax(score)], 100 * np.max(score))
    # )

# main function for testing purposes

# if __name__ == '__main__':
# print(sys.argv[1])
# model = keras.models.load_model("second_model")
# makePrediction(SONG_PATH)
# makePrediction(sys.argv[1], model)
