import keras
from keras import backend as K
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNetV2
from keras.applications.mobilenet import preprocess_input
import numpy as np
from keras.optimizers import Adam
from keras import metrics

import warnings
import cv2
import keras
from keras import models, layers, optimizers
from keras.applications import VGG16
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model
from keras.preprocessing import image as image_utils
from keras.utils import to_categorical


# TODO TENSORBOARD
def mobilenetv2(input_shape, include_top=False):
    base_model = MobileNetV2(input_shape=input_shape, weights='imagenet', include_top=include_top)  # The include_top = False removes bottleneck part

    x = base_model.output  # I guess output refers to output of the convolutonal portion since it is "topless"

    # So this layer (I think) is needed to connect the old convolutional base to the new dense-layer "head" and outputs
    # The convolutional part is said to find features of images so this layer is called the "feature extractor"
    x = GlobalAveragePooling2D()(x)

    # Add dense layers after the connectin layer so the model can learn complex functions and classify better
    x = Dense(1024,activation='relu')(x)  # dense layer 1
    x = Dense(1024,activation='relu')(x)  # dense layer 2
    x = Dense(512,activation='relu')(x)  # dense layer 3
    preds = Dense(12,activation='softmax')(x)  # dense layer 4 connected to final output layer with softmax activation

    # Now instantiate our new model. I don't understand why inputs is the base model input
    model = Model(inputs=base_model.input,outputs=preds)    # I guess "Model" is just an empty model keras provides

    # Freezing all of the base model layers.
    for layer in model.layers:
        layer.trainable=False

    # # Or we could freeze all but the 20 last ones to "fine-tune" the base model to our new data
    # # Note: the model was MUCH faster and a little better WITHOUT the fine-tuning. Lol.
    # for layer in model.layers[:20]:  # Up to last 20 layers are frozen
    #     layer.trainable=False
    # for layer in model.layers[20:]:  # Last 20 layers are not frozen
    #     layer.trainable=True

    # Compile model
    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy', 'loss'])

    # TODO Probably want to add in stuff for tensorboard here

    return model


def vgg16(input_shape, include_top):

    vgg_base = VGG16(weights='imagenet', include_top=include_top, input_shape=(input_shape))
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

    return model


