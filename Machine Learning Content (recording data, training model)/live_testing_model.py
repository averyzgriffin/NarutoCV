import sys
sys.path.append("..") # Adds higher directory to python modules path.
import cv2
import time
import numpy as np
from keras import models
import camera_ops


# --------------------------------------------------
# Global Variables
# --------------------------------------------------
saved_model = "VGG16_EPOCHS50_CODENAME_accumulative_data_4-9_1586483732.9708767"
model = models.load_model(saved_model)
WIDTH = 165
HEIGHT = 235


# ------
# Signs
# ------
bird = [1,0,0,0,0,0,0,0,0,0,0,0]
boar = [0,1,0,0,0,0,0,0,0,0,0,0]
dog = [0,0,1,0,0,0,0,0,0,0,0,0]
dragon = [0,0,0,1,0,0,0,0,0,0,0,0]
hare = [0,0,0,0,1,0,0,0,0,0,0,0]
horse = [0,0,0,0,0,1,0,0,0,0,0,0]
monkey = [0,0,0,0,0,0,1,0,0,0,0,0]
ox = [0,0,0,0,0,0,0,1,0,0,0,0]
ram = [0,0,0,0,0,0,0,0,1,0,0,0]
rat = [0,0,0,0,0,0,0,0,0,1,0,0]
serpent = [0,0,0,0,0,0,0,0,0,0,1,0]
tiger = [0,0,0,0,0,0,0,0,0,0,0,1]


signs = ['bird', 'boar', 'dog', 'dragon', 'hare', 'horse', 'monkey', 'ox', 'ram', 'rat', 'serpent', 'tiger']


print('---CAMERA STARTING. DONT MOVE---')
for i in list(range(3))[::-1]:
    print(i+1)
    time.sleep(1)


# -----------------
# MAIN FUNCTION
# -----------------
if __name__ == "__main__":

    num_frames, count = 0, 0
    calibrate_frames = 30
    aWeight = 0.5
    mean_cutoff = 6
    accumulated_predictions = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='float64')
    average_prediction = None
    top_predictions = None
    camera = camera_ops.setup_camera()


    while True:
        (grabbed, frame) = camera.read()

        # CAMERA BUTTON CONTROLS
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break

        # COMPUTER VISION OPERATIONS ON FRAME
        processed_frame, color_frame = camera_ops.process_frame(frame)
        (height, width) = processed_frame.shape[:2]

        if num_frames < calibrate_frames:  # 30 frames = 1 seconds ..... I think
            camera_ops.background_run_avg(processed_frame, aWeight)
        else:
            threshold = camera_ops.segment_hand_region(processed_frame)

            if threshold is not None:
                cv2.imshow("Threshold", threshold)
                threshold = np.stack((threshold,) * 3, axis=-1)  # Expand frame to 3 channels for the model

                prediction = model.predict([np.reshape(threshold, (1, height, width, 3))])
                accumulated_predictions += prediction

                labeled_prediction = signs[np.argmax(prediction)]
                print(labeled_prediction)

        num_frames += 1

    camera.release()
    cv2.destroyAllWindows()

