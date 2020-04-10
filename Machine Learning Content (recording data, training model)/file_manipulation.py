import shutil
import os
import numpy as np
from PIL import Image


def rename_files(directory):
    for count, filename in enumerate(os.listdir(directory)):
        count += 2200
        dst = "handsign_"+str(count)+".npy"
        src = directory+filename
        dst = directory+dst

        os.rename(src, dst)


def move_files(RootDir1, TargetFolder):
    for root, dirs, files in os.walk((os.path.normpath(RootDir1)), topdown=False):
            for name in files:
                if name.endswith('.npy'):
                    print("Found ", name)
                    SourceFolder = os.path.join(root,name)
                    shutil.copy2(SourceFolder, TargetFolder)  # copies files to new folder


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



source_dir = "E:/Artificial Intelligence/naruto/data-4-9-20-dr/"
# source2_dir = "E:/Artificial Intelligence/naruto/data-4-9-20-kt/"
training_dir = "E:/Artificial Intelligence/naruto/combined_training_data/"
# validation_dir = "E:/Artificial Intelligence/naruto/validation_data/"

convert_NPY(source_dir, training_dir)
# convert_NPY(source2_dir, training_dir)
