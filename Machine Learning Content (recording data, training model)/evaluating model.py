from keras_preprocessing.image import ImageDataGenerator
from keras import models
from keras.backend import clear_session
import numpy as np
from sklearn import metrics
import pandas as pd


saved_model_1 = "VGG16_EPOCHS50_CODENAME_accumulative_data_4-9_1586483732.9708767"
saved_model_2 = "VGG16_EPOCHS50_CODENAME_accumulative_data_4-9_actual_1586535508.2220433"
saved_models = [saved_model_1, saved_model_2]

clean_short_dir = "E:/Artificial Intelligence/naruto/testing_data/testing_data_clean_short"
noisy_short_dir = "E:/Artificial Intelligence/naruto/testing_data/testing_data_noisy_short"
test_dirs = [clean_short_dir, noisy_short_dir]

WIDTH = 165
HEIGHT = 235


def get_classification_report(model, eval_dir="E:/Artificial Intelligence/naruto/testing_data/", augment=False):

    model = models.load_model(model)

    if augment:
        test_generator = ImageDataGenerator(width_shift_range=[-.2,.2], height_shift_range=[-.15,.15],
                                            rotation_range=45, brightness_range=[.2,1.2], zoom_range=[.7,1.5])
    else:
        test_generator = ImageDataGenerator()

    test_it = test_generator.flow_from_directory(eval_dir, batch_size=32, shuffle=False, target_size=(HEIGHT, WIDTH))
    test_steps_per_epoch = np.math.ceil(test_it.samples / test_it .batch_size)

    predictions = model.predict_generator(test_it, steps=test_steps_per_epoch)
    predicted_classes = np.argmax(predictions, axis=1)

    true_classes = test_it.classes
    class_labels = list(test_it.class_indices.keys())

    report = metrics.classification_report(true_classes, predicted_classes, target_names=class_labels, output_dict=True)
    clear_session()
    return report


def save_report(report, name):
    df = pd.DataFrame(report).transpose()
    html = df.to_html()
    text_file = open(name + ".html", "w")
    text_file.write(html)
    text_file.close()


for saved_model in saved_models:
    for test_dir in test_dirs:
        for i in range(2):
            if i==0:
                report = get_classification_report(saved_model, test_dir)
                print(report)
            elif i==1:
                report = get_classification_report(saved_model, test_dir, augment=True)
                print(report)
            save_report(report, saved_model+"_"+test_dir[-11]+"_"+str(i))

