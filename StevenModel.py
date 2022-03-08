# https://www.tensorflow.org/tutorials/load_data/images
import tensorflow as tf
import os
from keras.preprocessing.image import ImageDataGenerator


imageHeight = 480
imageWidth = 640


trainingDataSet = tf.keras.utils.image_dataset_from_directory(
    directory='Spectrograms',
    labels='inferred',  # Default is 'inferred
    label_mode='categorical',  # [0, 0, 0, 0, 0 , 0, 0, 0, 1, 0]  
    batch_size=32,  # Default is 32
    image_size=(imageHeight, imageWidth),  # Default is (256, 256)
    validation_split=0.2,
    subset="training",  # options "training" or "validation"
    seed=123
)

### Display some examples of images from batch ###
# import matplotlib.pyplot as plt

# class_names = trainingDataSet.class_names

# plt.figure(figsize=(10, 10))
# for images, labels in trainingDataSet.take(1):
#     for i in range(9):
#         ax = plt.subplot(3, 3, i + 1)
#         plt.imshow(images[i].numpy().astype("uint8"))
#         print(labels[i])
#         plt.title(class_names[labels[i]])
#         plt.axis("off")

# plt.show()

# ## Print shape of batches ###
# for image_batch, labels_batch in trainingDataSet:
#     print(image_batch.shape)
#     print(labels_batch.shape)
#     break

validationDataSet = tf.keras.utils.image_dataset_from_directory(
    directory='Spectrograms',
    labels='inferred',
    label_mode='categorical',
    batch_size=32,  # Default is 32
    image_size=(imageHeight, imageWidth),  # Default is (256, 256)
    validation_split=0.2,
    subset="validation",
    seed=123
)

classNames = trainingDataSet.class_names
numClasses = len(classNames)

AUTOTUNE = tf.data.AUTOTUNE
trainingDataSet = trainingDataSet.cache().prefetch(buffer_size=AUTOTUNE)
validationDataSet = validationDataSet.cache().prefetch(buffer_size=AUTOTUNE)


model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1./255),
    tf.keras.layers.Conv2D(16, 3, activation="relu", input_shape=(32, 480, 640, 3)),
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
    optimizer='adam',
    loss=tf.losses.CategoricalCrossentropy(),
    metrics=['accuracy']
)

# ### Print model so far ###
# model.summary()



model.fit(
    trainingDataSet,
    validation_data=validationDataSet,
    epochs=30
)

# print(model.summary())


