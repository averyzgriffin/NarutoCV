import itertools


# --------------------------------------------------------------------------------------------------------------
# MODEL + PREDICTION FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def get_sequence_of_predictions(current_sequence, predictions):
    current_sequence.append(predictions)
    return current_sequence


def get_permutations_of_predictions(current_sequence):
    permutation = list(itertools.product(*current_sequence))
    return permutation


def get_top3_sign_predictions(labels, predictions):
    dict_pred = dict(zip(labels, predictions[0]))
    order_dict = {}
    top_signs = []
    top_signs_confidence_percents = []
    for key, value in sorted(dict_pred.items(), key=lambda item: item[1]):
        order_dict.update({key: value})
    for i in range(3):
        top_signs.append(list(order_dict)[-(i+1)])
        top_signs_confidence_percents.append(list(order_dict.values())[-(i+1)])

    return order_dict, top_signs, top_signs_confidence_percents
