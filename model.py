import json
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import os
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

DATA_PATH = "metadata.json"


def load_data(data_path):

    with open(data_path, "r") as fp:
        data = json.load(fp)

    X = np.array(data["mfcc"])
    y = np.array(data["labels"])
    return X, y


def plot_history(history):
    """
    Graphing function to show accuracy and loss data in train vs. test format.
    :param history:  Training data obtained from the model.:
    """

    figure, axis = plt.subplots(2)

    # graph for accuracy
    axis[0].plot(history.history["accuracy"], label="training accuracy")
    axis[0].plot(history.history["val_accuracy"], label="test accuracy")
    axis[0].set_ylabel("Accuracy")
    axis[0].legend(loc="lower right")
    axis[0].set_title("Accuracy")

    # graph for errors
    axis[1].plot(history.history["loss"], label="training error")
    axis[1].plot(history.history["val_loss"], label="test error")
    axis[1].set_ylabel("Error")
    axis[1].set_xlabel("Epoch")
    axis[1].legend(loc="upper right")
    axis[1].set_title("Error")

    plt.show()


def prepare_datasets(test_size, validation_size):

    # load data
    X, y = load_data(DATA_PATH)

    # create train, validation and test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=validation_size)

    # add an axis to input sets
    X_train = X_train[..., np.newaxis]
    X_validation = X_validation[..., np.newaxis]
    X_test = X_test[..., np.newaxis]

    return X_train, X_validation, X_test, y_train, y_validation, y_test


def build_model(input_shape):

    # build network topology
    model = keras.Sequential()

    # 1st Convolution Layer
    model.add(keras.layers.Conv2D(filters=64, kernel_size=(3, 3), input_shape=input_shape))
    model.add(keras.layers.LeakyReLU(alpha=0.001))
    model.add(keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # 2nd Convolution Layer
    model.add(keras.layers.Conv2D(filters=64, kernel_size=(3, 3), input_shape=input_shape))
    model.add(keras.layers.LeakyReLU(alpha=0.001))
    model.add(keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # 3rd Convolution Layer
    model.add(keras.layers.Conv2D(filters=64, kernel_size=(2, 2), input_shape=input_shape))
    model.add(keras.layers.LeakyReLU(alpha=0.001))
    model.add(keras.layers.MaxPooling2D((2, 2), strides=(2, 2), padding='same'))
    model.add(keras.layers.BatchNormalization())

    # Flatten and Run Through Dense Layer
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64))
    model.add(keras.layers.LeakyReLU(alpha=0.001))
    model.add(keras.layers.Dropout(0.3))

    # One Last Dense Layer for Output
    model.add(keras.layers.Dense(10, activation='softmax'))

    return model


def predict(model, X, y):
    """Predict a single sample using the trained model
    :param model: Trained classifier
    :param X: Input data
    :param y (int): Target
    """

    # add a dimension to input data for sample - model.predict() expects a 4d array in this case
    X = X[np.newaxis, ...] # array shape (1, 130, 13, 1)

    # perform prediction
    prediction = model.predict(X)

    # get index with max value
    predicted_index = np.argmax(prediction, axis=1)

    print("Target: {}, Predicted label: {}".format(y, predicted_index))


if __name__ == "__main__":

    # get train, validation, test splits
    X_train, X_validation, X_test, y_train, y_validation, y_test = prepare_datasets(0.25, 0.2)

    # create network
    input_shape = (X_train.shape[1], X_train.shape[2], 1)
    model = build_model(input_shape)

    # compile model
    optimiser = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimiser,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    # early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

    # training function
    # history = model.fit(X_train, y_train, validation_data=(X_validation, y_validation),
    #                     batch_size=32, epochs=30)

    history = model.fit(X_train, y_train, batch_size=32, epochs=30)

    # plot accuracy/error for training and validation
    plot_history(history)

    print("\n")
    print(model.metrics_names)
    print("\n")

    # evaluate model on test set
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    print('\nTest accuracy:', test_accuracy)
