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
from keras.applications.mobilenet import preprocess_input
import numpy as np
from keras.optimizers import Adam
from IPython.display import Image
from google_images_download import google_images_download
from model import mobilenetv2, vgg16
from keras.backend import clear_session
from datetime import date
from random import shuffle


clear_session()


def process_data(x_data):
    # x_data = np.array(x_data, dtype = 'float32')
    x_data = np.stack((x_data,)*3, axis=-1)

    x_data /= 255
    # y_data = np.array(y_data)
    # y_data = to_categorical(y_data)
    return x_data


# TODO Check each run
FILE_I_END = 299

WIDTH = 165
HEIGHT = 235
LR = .0003
EPOCHS = 2
batch = 60

LOAD_MODEL = False  # This should be false if we are training a fresh new model
MODEL_NAME = f'VGG16_LR_{LR}_EPOCHS{EPOCHS}_date{date.today()}'
PREV_MODEL = ''
# model = mobilenetv2(input_shape=(HEIGHT,WIDTH,3), include_top=False)
model = vgg16(input_shape=(WIDTH,HEIGHT,3), include_top=False)

# Tensorboard
logdir = "./log_adam/"
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)


if LOAD_MODEL:
    model.load(PREV_MODEL)
    MODEL_NAME = PREV_MODEL
    print('We have loaded a previous model!!!!')
else:
    print("No previous model found....creating new one")


for e in range(EPOCHS):
    data_order = [i for i in range(1, FILE_I_END + 1)]
    shuffle(data_order)
    for count, i in enumerate(data_order):

        try:
            # Location of training data; on my E drive TODO check each training session
            file_name = f"E:/naruto/data-10-13/all_avery/handsign_{i}.npy"

            data = np.load(file_name, allow_pickle=True)
            print(f'handsign_{i}.npy Length: ', len(data))

            train = data
            # test = data[-10:]

            X = np.array([i[0] for i in train], dtype='float32').reshape((-1, WIDTH, HEIGHT))
            Y = np.array([i[1] for i in train])

            # test_x = np.array([i[0] for i in test], dtype='float32').reshape((-1, WIDTH, HEIGHT))
            # test_y = np.array([i[1] for i in test])

            X = np.stack((X,) * 3, axis=-1)
            X /= 255
            # test_x = np.stack((test_x,) * 3, axis=-1)
            # test_x /= 255

            model.fit(X, Y, epochs=1, batch_size=32, validation_split=.10, verbose=1,
                      callbacks=[tensorboard_callback])
            # model.fit({'input': X}, {'targets': Y}, batch_size=batch, n_epoch=1,
            #           validation_set=({'input': test_x}, {'targets': test_y}),
            #           snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)

            # if count % 10 == 0:  # Make sure to have at least 10 saves for training
            #     print('SAVING MODEL!')
            #     model.save(MODEL_NAME)

        except Exception as e:
            print(str(e))


clear_session()

# tensorboard --logdir C:/path/to/log --host=127.0.0.1    #type localhost:6006 into browser
