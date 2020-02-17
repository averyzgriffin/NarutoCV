import itertools
import global_variables as glob_var
import numpy as np


# --------------------------------------------------------------------------------------------------------------
# MODEL + PREDICTION FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def get_top3_predictions(ordered_predictions):
    top_signs, top_signs_percents = [], []
    for i in range(3):
        top_signs.append(list(ordered_predictions)[-(i+1)])  # I think this grabs the top 3 keys from reverse ordered dictionary
        top_signs_percents.append(list(ordered_predictions.values())[-(i+1)])  # I think this grabs the top 3 values

    return top_signs, top_signs_percents


def order_predictions(labeled_predictions):
    ordered_predictions = {}
    for key, value in sorted(labeled_predictions.items(), key=lambda item: item[1]):  # I think this sorts the pred_dict by value
        ordered_predictions.update({key: value})

    return ordered_predictions


def label_predictions(labels, predictions):
    labeled_predictions = dict(zip(labels, predictions[0]))

    return labeled_predictions


def get_sequence_of_predictions(current_sequence, predictions):
    current_sequence.append(predictions)

    return current_sequence


def get_permutations_of_predictions(current_sequence):
    permutation = list(itertools.product(*current_sequence))

    return permutation


def get_top3_signs(labels, predictions):
    labeled_predictions = label_predictions(labels, predictions)  # {'bird': 4.585343e-33, 'label': prediction, etc.]
    ordered_predictions = order_predictions(labeled_predictions)
    top_signs, top_signs_percents = get_top3_predictions(ordered_predictions)

    return top_signs


def get_predictions(accumulated_predictions, prediction, sequence):
    average_prediction = accumulated_predictions / glob_var.mean_cutoff
    accumulated_predictions = np.zeros_like(prediction)
    top_signs = get_top3_signs(glob_var.signs, average_prediction)
    sequence = get_sequence_of_predictions(sequence, top_signs)

    return accumulated_predictions, sequence, top_signs

