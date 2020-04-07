import shutil
import os
import numpy as np
from PIL import Image
import cv2


sourceDir = r'E:/Artificial Intelligence/naruto/data-2-25-20/avery/'
targetFolder = r'E:/Artificial Intelligence/naruto/data-2-25-20/all_avery/'


def move_files(RootDir1, TargetFolder):
    for root, dirs, files in os.walk((os.path.normpath(RootDir1)), topdown=False):
            for name in files:
                if name.endswith('.npy'):
                    print("Found ", name)
                    SourceFolder = os.path.join(root,name)
                    shutil.copy2(SourceFolder, TargetFolder)  # copies files to new folder


source1_dir = "E:/Artificial Intelligence/naruto/data-4-6-20/"
source2_dir = "E:/Artificial Intelligence/naruto/data-10-13/"
training_dir = "E:/Artificial Intelligence/naruto/training_data/"
validation_dir = "E:/Artificial Intelligence/naruto/validation_data/"

def convert_NPY(sourcedir, newdir):
    for root, dirs, files in os.walk((os.path.normpath(sourcedir)), topdown=False):
        for dir in dirs:
            print(dir.upper())
            for file in os.listdir(sourcedir + dir):
                print(file)
                data = np.load(sourcedir+dir+'/'+file, allow_pickle=True)
                for i in range(len(data)):
                    image = data[i][0]
                    image = Image.fromarray(image)
                    image.save(newdir+dir+'/' + f"{file}_{i}.jpg", "JPEG")


convert_NPY(source1_dir, training_dir)
# convert_NPY(source2_dir, validation_dir)
