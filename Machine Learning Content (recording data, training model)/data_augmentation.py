from numpy import expand_dims
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot


# load the image
dir_train = "E:/Artificial Intelligence/naruto/combined_training_data/"
dir_image = 'rat/handsign_2432.npy_48.jpg'
data = load_img(dir_train+dir_image)


def augment(img, aug_type=None, aug_value=None):
	img_array = img_to_array(img)
	samples = expand_dims(img_array, 0)

	if aug_type == "w_shift":
		datagen = ImageDataGenerator(width_shift_range=aug_value)  # [-0.1,0.1]
	elif aug_type == "h_shift":
		datagen = ImageDataGenerator(height_shift_range=aug_value)  # [-0.1,0.1]
	elif aug_type == "rotate":
		datagen = ImageDataGenerator(rotation_range=aug_value)  # 45  degrees of 365
	elif aug_type == "brighten":
		datagen = ImageDataGenerator(brightness_range=aug_value)  # [0.2,1.8]  dark-brighten
	elif aug_type == "zoom":
		datagen = ImageDataGenerator(zoom_range=aug_value)  # [.8,1.2]  zoom in, zoom out
	elif aug_type == "zca":
		datagen = ImageDataGenerator(zca_whitening=True)  # True/False

	it = datagen.flow(samples, batch_size=1)

	for i in range(9):
		pyplot.subplot(330 + 1 + i)
		batch = it.next()
		image = batch[0].astype('uint8')
		pyplot.imshow(image)
	pyplot.show()


augment(data, 'w_shift', [-.2,.2])
augment(data, 'h_shift', [-.15,.15])
augment(data, 'rotate', 15)
augment(data, 'brighten', [.8,1.2])
augment(data, 'zoom', [.7,1.5])
# augment(data, 'zca')


