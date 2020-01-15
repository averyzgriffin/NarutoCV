import os
import numpy as np


"""
def process_image(path):
    img = Image.open(path)
    img = img.resize((224, 224))
    img = np.array(img)
    return img


def process_data(X_data, y_data):
    X_data = np.array(X_data, dtype = 'float32')
    X_data = np.stack((X_data,)*3, axis=-1)
    X_data /= 255
    return X_data, y_data


# 'E:/naruto/data-10-13/avery/'
def walk_file_tree(relative_path):
    X_data = []
    y_data = []
    for directory, subdirectories, files in os.walk(relative_path):
        for file in files:
            if not file.startswith('.') and (not file.startswith('C_')):
                path = os.path.join(directory, file)
                # gesture_name = gestures[file[0:2]]
                # y_data.append(gestures_map[gesture_name])
                X_data.append(process_image(path))

            else:
                continue

    X_data, y_data = process_data(X_data, y_data)
    return X_data, y_data
"""

# TODO Check each run
FILE_I_END = 25

WIDTH = 165
HEIGHT = 235
LR = .0003
EPOCHS = 2
batch = 5


def process_data(X_data):
    X_data = np.array(X_data, dtype='float32')
    X_data = np.stack((X_data,) * 3, axis=-1)
    X_data /= 255
    return X_data


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
    X_data = process_data(X_data=X_data)
    return X_data, y_data


X, Y = walk_file_tree()
print(X.shape)  # (30000, 235, 165, 3)
print(Y[0])  # [1,0,0,0,0,0,0,0,0,0,0,0]
