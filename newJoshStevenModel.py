import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd

imageHeight = 149
imageWidth = 200


def plotValidate(history):
    pd.DataFrame(history.history).plot(figsize=(12, 6))
    plt.show()



def createDataset():
    specList = []
    genreList = []
    genres = "blues classical country hiphop jazz metal pop reggae rock"
    for g in genres.split():
        # loop through the genres directory
        # and pick the wav file from each genre directory
        for filename in os.listdir(f'./noDiscoClean/{g}'):
            if filename == ".DS_Store":
                pass
            else:
                img = keras.utils.load_img(
                    f'./noDiscoClean/{g}/{filename}', target_size=(imageHeight, imageWidth)
                )
                img_array = keras.utils.img_to_array(img)
                specList.append(img_array)
                genreList.append(g)
    specList = np.array(specList)
    genreList = np.array(genreList)
    return specList, genreList


def stringToNumber(param):
    if param == "blues":
        return 0
    elif param == "classical":
        return 1
    elif param == "country":
        return 2
    elif param == "hiphop":
        return 3
    elif param == "jazz":
        return 4
    elif param == "metal":
        return 5
    elif param == "pop":
        return 6
    elif param == "reggae":
        return 7
    elif param == "rock":
        return 8
    else:
        return False


def convertGenres(genreList):
    newList = []
    for x in genreList:
        a = stringToNumber(x)
        newList.append(a)
    newList = np.array(newList)
    return newList


if __name__ == '__main__':
    X, y = createDataset()

    y = convertGenres(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    y_cat_train = tf.keras.utils.to_categorical(y_train)
    y_cat_test = tf.keras.utils.to_categorical(y_test)

    X_train = X_train/255

    X_test = X_test/255

    model = tf.keras.Sequential([
        # tf.keras.layers.Rescaling(1./255),

        tf.keras.layers.Conv2D(filters=64, kernel_size=(4, 4), input_shape=(imageHeight, imageWidth, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Dropout(0.8),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(100, activation="relu"),

        tf.keras.layers.Dense(9, activation="softmax")
    ])

    callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0004), loss=tf.losses.CategoricalCrossentropy(),
                  metrics=['accuracy'])

    print(model.summary())

    history = model.fit(X_train, y_cat_train,
                        batch_size=6,
                        validation_split=0.2,
                        epochs=15)

    plotValidate(history)
    print("\n\n")
    print("MODEL EVALUATION:")
    model.evaluate(X_test, y_cat_test, batch_size=1, verbose=1)

    model.save("second_model")
