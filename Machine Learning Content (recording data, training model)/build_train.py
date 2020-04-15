import keras
import numpy as np
from keras.backend import clear_session
from datetime import date
from keras.callbacks import ModelCheckpoint
import warnings
from keras import models, layers, optimizers
from keras.applications import VGG16
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
import os
import time
from PIL import Image


clear_session()


def process_data(X_data, y_data):
    X_data = np.array(X_data, dtype='float32')

    X_data = np.stack((X_data,) * 3, axis=-1)

    X_data /= 255
    y_data = np.array(y_data)
    return X_data, y_data


def walk_file_tree(dir):
    X_data = []
    y_data = []
    for directory, subdirectories, files in os.walk(dir):
        for file in files:
            if not file.startswith('.') and (not file.startswith('C_')) and (not file.startswith('handsign_5')):
                path = os.path.join(directory, file)
                data = np.load(path, allow_pickle=True)
                for image_event in data:
                    X_data.append(image_event[0])
                    y_data.append(image_event[1])

    print('done walking, time to process')
    X_data, y_data = process_data(X_data=X_data, y_data=y_data)
    print('done processing')
    return X_data, y_data


# ------------------------
# Global Variables
# ------------------------
X, Y = walk_file_tree("E:/Artificial Intelligence/naruto/data-2-25-20/all_avery/")

WIDTH = 165
HEIGHT = 235
LR = .0003
EPOCHS = 3
batch = 32  # memory limit varies. used to be 60 but 32 seems to be the safe bet.
MODEL_NAME = f'VGG16_LR_{LR}_EPOCHS{EPOCHS}_{time.time()}'
PREV_MODEL = ''


# ------------------------
# Import and Build Model
# ------------------------
vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=(HEIGHT,WIDTH,3))
optimizer = optimizers.Nadam()

base_model = vgg_base  # Topless
# Add top layer
x = base_model.output
x = Flatten()(x)
x = Dense(128, activation='relu', name='fc1')(x)
x = Dense(128, activation='relu', name='fc2')(x)
x = Dense(128, activation='relu', name='fc3')(x)
x = Dropout(0.5)(x)
x = Dense(64, activation='relu', name='fc4')(x)
predictions = Dense(12, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Train top layers only
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Tensorboard
logdir = f"log_test123/"
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
checkpoint = ModelCheckpoint(MODEL_NAME, monitor='val_loss', save_best_only=True, mode='min')


# for e in range(EPOCHS):
model.fit(X, Y, epochs=EPOCHS, batch_size=batch, validation_split=.20, verbose=1,
          callbacks=[tensorboard_callback, checkpoint], shuffle=True,)


clear_session()

# tensorboard --logdir C:/path/to/log --host=127.0.0.1    #type localhost:6006 into browser
