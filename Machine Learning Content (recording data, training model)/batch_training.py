from keras_preprocessing.image import ImageDataGenerator
import keras
from keras.backend import clear_session
from datetime import date
from keras.callbacks import ModelCheckpoint
from keras import models, layers, optimizers
from keras.applications import VGG16
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
import time


# Parameters
training_data_codename = "2-25+4-06"
dir_train = "E:/Artificial Intelligence/naruto/training_data/"
dir_val = "E:/Artificial Intelligence/naruto/validation_data/"
num_images = 600*100
WIDTH = 165
HEIGHT = 235


EPOCHS = 10
batch_size = 48
MODEL_NAME = f'VGG16_EPOCHS{EPOCHS}_CODENAME_{training_data_codename}_{time.time()}'
PREV_MODEL = ''

# Data Generator
datagen = ImageDataGenerator()
train_it = datagen.flow_from_directory(dir_train, batch_size=batch_size, target_size=(HEIGHT, WIDTH))
val_it = datagen.flow_from_directory(dir_val, batch_size=batch_size, target_size=(HEIGHT, WIDTH))
test_it = None



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

# Compile Model
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Tensorboard
logdir = f"log_generator/"
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
checkpoint = ModelCheckpoint(MODEL_NAME, monitor='val_loss', save_best_only=True, mode='min')


# Model Fit
model.fit_generator(train_it, steps_per_epoch=num_images/batch_size, epochs=10, validation_data=val_it, validation_steps=num_images/batch_size, callbacks=[tensorboard_callback, checkpoint])

clear_session()
