import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow import keras
from keras.models import Sequential

# to avoid Tensorflow startup messages in terminal
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}


def trainModel(model, optimizer, X_train, y_train, X_test, y_test):
    batch_size = 128
    model.compile(optimizer=optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics='accuracy')

    return model.fit(X_train, y_train, validation_data=(X_test, y_test),
                     batch_size=batch_size, epochs=600, verbose=1)


def plotValidate(history):
    print("Validation Accuracy", max(history.history["val_accuracy"]))
    pd.DataFrame(history.history).plot(figsize=(12, 6))
    plt.show()


def buildModel(X_train):

    input_shape = (X_train.shape[1], )

    model = Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=input_shape),
        keras.layers.BatchNormalization(),

        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),

        keras.layers.Dense(128, activation='relu'),
        keras.layers.BatchNormalization(),

        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.2),

        keras.layers.Dense(10, activation='softmax'),
    ])

    return model


if __name__ == '__main__':
    df = pd.read_csv("features_3_sec.csv")
    df = df.drop(['filename', 'length'], axis=1)

    # slice off class list at end of csv and encode for y axis
    class_list = df.iloc[:, -1]
    convertor = LabelEncoder()
    y = convertor.fit_transform(class_list)

    # scale X axis
    fit = StandardScaler()
    X = fit.fit_transform(np.array(df.iloc[:, :-1], dtype=float))

    # populate test and train data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25)

    # build and train model
    model = buildModel(X_train)
    history = trainModel(model, 'adam', X_train, y_train, X_test, y_test)

    # evaluate model accuracy and display in easy to read format
    test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=128)

    print("The test loss is: ", test_loss)
    print("The test accuracy is: ", test_acc * 100)

    plotValidate(history)

    # # save model for later use (uncomment only when you want to create a new model
    # model.save("my_model")
