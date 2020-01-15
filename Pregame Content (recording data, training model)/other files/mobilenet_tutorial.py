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
from IPython.display import Image
from google_images_download import google_images_download


# Loading the pre-trained model which will act as base
mobile = MobileNetV2()


# --------------------------------------
# TESTING MODEL ON KNOWN TYPES OF IMAGES
# --------------------------------------
def prepare_image(file):
    img_path = ''
    img = image.load_img(img_path + file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)


Image(filename='German_Shepherd.jpg')
preprocessed_image = prepare_image('German_Shepherd.jpg')
predictions = mobile.predict(preprocessed_image)
results = imagenet_utils.decode_predictions(predictions)
print(results)

for i in range(5):
    print()

# --------------------
# Download image data
# --------------------
# response = google_images_download.googleimagesdownload()
# arguments = {"keywords":"blue tit","limit":100,"print_urls":False,"format":"jpg", "size":">400*300"}
# paths = response.download(arguments)
# arguments = {"keywords":"crow","limit":100,"print_urls":False, "format":"jpg", "size":">400*300"}
# paths = response.download(arguments)


# -----------------------
# Building the new model
# -----------------------
base_model = MobileNetV2(weights='imagenet', include_top=False)  # I believe the include_top = False removes bottleneck

x = base_model.output  # I guess output refers to output of the convolutonal portion since it is "topless"

# So this layer (I think) is needed to connect the old convolutional base to the new dense-layer "head" and outputs
# The convolutional part is said to find features of visual information so this layer is called the "feature extractor"
x = GlobalAveragePooling2D()(x)

# Add dense layers after the connectin layer so the model can learn complex functions and classify better
x = Dense(1024,activation='relu')(x)  # dense layer 1
x = Dense(1024,activation='relu')(x)  # dense layer 2
x = Dense(512,activation='relu')(x)  # dense layer 3
preds = Dense(2,activation='softmax')(x)  # dense layer 4 connected to final output layer with softmax activation


# Now instantiate our new model. I don't understand why inputs is the base model input
model = Model(inputs=base_model.input,outputs=preds)    # I guess "Model" is just an empty model keras provides

# Printing out the architecture of model
for i,layer in enumerate(model.layers):
    print(i,layer.name)
for i in range(5):
    print()

# Freezing all of the base model layers.
for layer in model.layers:
    layer.trainable=False

# # Or we could freeze all but the 20 last ones to "fine-tune" the base model to our new data
# # Note: the model was MUCH faster and a little better WITHOUT the fine-tuning. Lol.
# for layer in model.layers[:20]:  # Up to last 20 layers are frozen
#     layer.trainable=False
# for layer in model.layers[20:]:  # Last 20 layers are not frozen
#     layer.trainable=True


# Creating our data batches
train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies

train_generator=train_datagen.flow_from_directory(r'C:\Users\Avery\Desktop\handrecognition\downloads',
                                                 target_size=(224,224),
                                                 color_mode='rgb',
                                                 batch_size=2,
                                                 class_mode='categorical',
                                                 shuffle=True)

# Compile model
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
step_size_train = train_generator.n//train_generator.batch_size

# Train model
model.fit_generator(generator=train_generator, steps_per_epoch=step_size_train, epochs=10)
