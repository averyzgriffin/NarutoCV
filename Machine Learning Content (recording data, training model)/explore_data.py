import numpy as np
import cv2
import os


folder = "E:/Artificial Intelligence/naruto/data-2-25-20/all_avery/"

# data = np.load(folder + 'handsign_170.npy', allow_pickle=True)
# print(data.shape)
# print(data[0].shape) # first data point
# print(data[1].shape) # second data point
# print(data[0][0].shape) # fist data point image
# print(data[0][1]) # first data point label
# print(data[:,0]) # All images
# print(data[:,1]) # All labels
# print(len(data)) # 100 images per file

# print(data[:][0]) # First data point?
# print('2: ', data[0][:]) # First data point again?

for i in range(28):
    data = np.load(folder + f"handsign_{np.random.randint(300,599)}.npy", allow_pickle=True)
    image = data[np.random.randint(0,99),0]
    cv2.imshow(f'window{i}', image)
    if i < 7:
        cv2.moveWindow(f'window{i}', 700+175*i, 10)
    elif 7 <= i < 13:
        cv2.moveWindow(f'window{i}', 700+175*(i-6), 250)
    elif 13 <= i < 20:
        cv2.moveWindow(f'window{i}', 700+175*(i-13), 500)
    elif 20 <= i < 28:
        cv2.moveWindow(f'window{i}', 700+175*(i-20), 750)

cv2.waitKey(0)
cv2.destroyAllWindows()
