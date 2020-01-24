import itertools


# --------------------------------------------------------------------------------------------------------------
# MODEL + PREDICTION FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def get_sequence_of_predictions(current_sequence, predictions):
    seq = current_sequence
    pred = predictions
    seq.append(pred)

    return seq


def get_permutations_of_predictions(current_sequence):
    seq = current_sequence
    perm = list(itertools.product(*seq))

    return perm


def get_top3_sign_predictions(labels, predictions):
    dict_pred = dict(zip(labels, predictions[0]))
    order_dict = {}
    top_signs = []
    top_percents = []
    for key, value in sorted(dict_pred.items(), key=lambda item: item[1]):
        order_dict.update({key: value})
    for i in range(3):
        top_signs.append(list(order_dict)[-(i+1)])
        top_percents.append(list(order_dict.values())[-(i+1)])

    return order_dict, top_signs, top_percents
