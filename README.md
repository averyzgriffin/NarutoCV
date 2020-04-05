![alt text](https://github.com/AveryGriffin/NarutoCV/blob/master/extras/mainscreen.PNG)

Hello! Here is a machine learning + Pygame joint project.

The aim was to recreate the classic Naruto Arena turn-based strategy game....but with a twist. Instead of just using a mouse and keyboard to play the game, I incorporated the camera via computer vision. Specifically, the 'attacks' are preformed by weaving Naruto-style handsigns with your actual hands!

I wanted to bring alive the all-too-exciting handsigns from Naruto (remember when Zabuza and Kakashi whipped out Water Dragon Jutsu?!). And while my attempt is crude, funny, and not quite up to the level of the actual show....it's at least an attempt :).


Some details for anyone wanting to play:
The game uses the camera on your computer, so make sure to have one. Basically, there are 2 phases in the game: pre-jutsu phase and jutsu phase. In the pre-jutsu phase, Player 1 or 2 will select a jutsu and a character to attack. Then in the jutsu phase, the camera is fired up, video footage is taken, and some background code starts to track your hands (basically). Then it's just a matter of performing the prompted handsigns to activate the jutsu.

FYI: The camera is only open during the jutsu phase.


Calibrating the camera:
Each time the camera opens, their is a small time period where the camera needs to be calibrated. This is where the computer vision part is coming into play. Just make sure NOT to move during this phase and DO NOT have your hands in camera view at this point (raise them to your side for example). If you fail to hide your hands during calibration, the camera will not be able to track you hands properly. Calibration should only take 5 or so seconds. But it does need to happen each attack (jutsu) phase.


Techical details:
Everything was coded in Python.

The VGG16 convolutional neural network (by K. Simonyan and A. Zisserman) was used as the model.

Keras (TensorFlow) was used to train the model.

The model itself was only trained to perform handsign recognition, not segmentation. Meaning, nothing is actually tracking your hands. Instead, the camera performs image thresholding (to make the video feed black and white), then a running-average to segment the background from the forground, then a subtraction to remove the background. The result (if done correctly) is a video feed that only tracks movement (hands). And that movement is white against a black background. This black and white footage is then fed into the model.

And the game itself was coded using Pygame.

<p>&nbsp
&nbsp
&nbsp</p>

Woohoo!


Disclaimer:

Naruto-Arena - I took a lot of inspiration from the Naruto Arena game, so a lot of credit goes to them. Some of the icons used in my game are taken directly from their site. I definitely do not own any of those assets. Naruto-Arena.net itself is a fansite based on the Naruto Anime and Manga series. Unfortunately, I believe the game is no longer active (RIP). Here is the site https://naruto-arena.net/

VGG16 - This model is by K. Simonyan and A. Zisserman as mentioned. Here is the paper https://arxiv.org/abs/1409.1556

Computer Vision - The computer vision operations used to obtain the thresholded image were not of my own creation. It was a combination of stuff I knew and some stuff I picked up across the internet. A major help with solving this problem was Brenner Heintz in his article here https://towardsdatascience.com/training-a-neural-network-to-detect-gestures-with-opencv-in-python-e09b0a12bdf1. A matter of fact, it was Brenner's article that convinced me to switch from the Google Inception model to the VGG16 model (Inception was just not training properly).



And just to reiterate, the holders of the copyrighted and/or trademarked material appearing on this project are as follows:
NARUTO © 2002 MASASHI KISHIMOTO. All Rights Reserved.
