from keras.models import Sequential
import pandas as pd
import matplotlib.pyplot as plt


def train_model(models, epochs, optimizer):
    batch_size = 128
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics = 'accuracy')
    
    return model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs = epochs, batch_size = batch_size)



def plot_validate(history):
    print('Validation Accuracy', max(history.history['val_accuracy']))
    pd.DataFrame(history.history).plot(figsize(12,6))
    plt.show()  

def make_model():
    return model = 
      
