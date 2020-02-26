import cv2
import numpy as np
from PIL import Image
import os


for i in range(300):
    if i % 12 == 0:
        file = np.load(f"E:/Artificial Intelligence/naruto/data-10-13/all_avery/handsign_{i}.npy", allow_pickle=True)
        img = file[50][0]
        im = Image.fromarray(img)
        im.save("C:/Users/Avery/Desktop/narutoimages/" + f'{i}.png')

