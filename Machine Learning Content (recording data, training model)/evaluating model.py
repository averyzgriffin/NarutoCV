from keras_preprocessing.image import ImageDataGenerator
from keras import models, layers, optimizers
import numpy as np
from sklearn import metrics
import pandas as pd


saved_model_1 = "VGG16_EPOCHS10_CODENAME_2-25+4-06_1586224978.494585"
saved_model_2 = "VGG16_LR_0.0003_EPOCHS10_CODENAME_2-25_1586194069.8080373"
saved_model_3 = "VGG16_LR_0.0003_EPOCHS1_1571499473.7668839"
saved_models = [saved_model_1, saved_model_2, saved_model_3]

clean_long_dir = "E:/Artificial Intelligence/naruto/testing_data/testing_data_clean_long"
clean_short_dir = "E:/Artificial Intelligence/naruto/testing_data/testing_data_clean_short"
noisy_long_dir = "E:/Artificial Intelligence/naruto/testing_data/testing_data_noisy_long"
noisy_short_dir = "E:/Artificial Intelligence/naruto/testing_data/testing_data_noisy_short"
test_dirs = [clean_long_dir, clean_short_dir, noisy_long_dir, noisy_short_dir]

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
    return report


def save_report(report, name):
    df = pd.DataFrame(report).transpose()
    html = df.to_html()
    text_file = open(name + ".html", "w")
    text_file.write(html)
    text_file.close()


report1 = get_classification_report(saved_model_1, "E:/Artificial Intelligence/naruto/testing_data/testing_data_clean_long", augment=True)
print(report1)
save_report(report1, saved_model_1)

# for saved_model in saved_models:
#     for test_dir in test_dirs:
#         report = get_classification_report(saved_model, test_dir)
#         print(report)
#         save_report(report)

