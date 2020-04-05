import numpy as np
import cv2


data = np.load('testfolder01/handsign_69.npy', allow_pickle=True)
# print(data.shape)
# print(data[0].shape) # first data point
# print(data[1].shape) # second data point
# print(data[0][0].shape) # fist data point image
# print(data[0][1]) # first data point label
# print(data[:][0]) # First data point
# print('2: ', data[0][:]) # First data point again?
# print(data[:,0]) # All images
# print(data[:,1]) # All labels
# print(len(data)) # 10

for i in range(len(data)):
    image = data[i,0]
    cv2.imshow(f'window{i}', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
