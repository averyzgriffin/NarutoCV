import shutil
import os

RootDir1 = r'E:/naruto/data-10-13/avery/'
TargetFolder = r'E:/naruto/data-10-13/all_avery/'
for root, dirs, files in os.walk((os.path.normpath(RootDir1)), topdown=False):
        for name in files:
            if name.endswith('.npy'):
                print("Found ", name)
                SourceFolder = os.path.join(root,name)
                shutil.copy2(SourceFolder, TargetFolder)  # copies files to new folder

