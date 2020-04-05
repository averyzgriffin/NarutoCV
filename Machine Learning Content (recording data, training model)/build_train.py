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


clear_session()


def process_data(X_data, y_data):
    X_data = np.array(X_data, dtype='float32')
    X_data = np.stack((X_data,) * 3, axis=-1)
    X_data /= 255
    y_data = np.array(y_data)
    return X_data, y_data


# Get data
def walk_file_tree(dry="E:/naruto/data-10-13/all_avery"):
    X_data = []
    y_data = []
    for directory, subdirectories, files in os.walk(dry):
        for file in files:
            if not file.startswith('.') and (not file.startswith('C_')):
                path = os.path.join(directory, file)
                data = np.load(path, allow_pickle=True)
                for observation in data:
                    X_data.append(observation[0])
                    y_data.append(observation[1])
                del data
                del path

    print('done walking, time to process')
    X_data, y_data = process_data(X_data=X_data, y_data=y_data)
    print('done processing')
    return X_data, y_data


# ------------------------
# Global Variables
# ------------------------
# TODO Check each run
X, Y = walk_file_tree()

input('Ready to build & compile?')
WIDTH = 165
HEIGHT = 235
LR = .0003
EPOCHS = 1
batch = 32  # 60 is limit I think
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
logdir = f"log/"
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
checkpoint = ModelCheckpoint(MODEL_NAME, monitor='val_loss', save_best_only=True, mode='min')


# for e in range(EPOCHS):
model.fit(X, Y, epochs=EPOCHS, batch_size=batch, validation_split=.20, verbose=1,
          callbacks=[tensorboard_callback, checkpoint], shuffle=True,)


clear_session()

# tensorboard --logdir C:/path/to/log --host=127.0.0.1    #type localhost:6006 into browser
