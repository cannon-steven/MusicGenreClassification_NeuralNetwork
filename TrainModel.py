import tensorflow as tf


def train_model(input_directory="Spectrograms",
                output_directory="MusicClassifier", image_height=369,
                image_width=496, num_channels=3, batch_size=10):
    """
    Trains a model to recognize genres on a set of spectrograms
    """

    trainingDataSet = tf.keras.utils.image_dataset_from_directory(
        directory=input_directory,
        labels='inferred',  # Default is 'inferred
        label_mode='categorical',  # [0, 0, 0, 0, 0 , 0, 0, 0, 1, 0]
        batch_size=batch_size,  # Default is 32
        image_size=(image_height, image_width),  # Default is (256, 256)
        validation_split=0.2,
        subset="training",  # options "training" or "validation"
        seed=123
    )

    validationDataSet = tf.keras.utils.image_dataset_from_directory(
        directory=input_directory,
        labels='inferred',
        label_mode='categorical',
        batch_size=batch_size,  # Default is 32
        image_size=(image_height, image_width),  # Default is (256, 256)
        validation_split=0.2,
        subset="validation",
        seed=123
    )

    classNames = trainingDataSet.class_names
    numClasses = len(classNames)

    AUTOTUNE = tf.data.AUTOTUNE
    trainingDataSet = trainingDataSet.cache().prefetch(buffer_size=AUTOTUNE)
    validationDataSet = validationDataSet.cache().prefetch(
        buffer_size=AUTOTUNE)

    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Resizing(149, 200),
        tf.keras.layers.Conv2D(
            8,
            3,
            activation="relu",
            input_shape=(batch_size, image_height, image_width, num_channels)
        ),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(16, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),


        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),


        tf.keras.layers.Conv2D(64, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),


        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(numClasses, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss=tf.losses.CategoricalCrossentropy(),
        metrics=['accuracy']
    )

    model.build((batch_size, image_height, image_width, num_channels))
    model.summary()

    model.fit(
        trainingDataSet,
        validation_data=validationDataSet,
        epochs=30
    )

    model.save(output_directory)
