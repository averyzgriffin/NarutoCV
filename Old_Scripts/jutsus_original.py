import cv2
from ffpyplayer.player import MediaPlayer


def jutsu(video):
    print('FIRE BALL')
    cap = cv2.VideoCapture(video)
    player = MediaPlayer(video)

    while True:
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()

        if not ret:
            break
        if cv2.waitKey(25) & 0xFF == 27:
            break

        cv2.imshow('frame',frame)

        if val != 'eof' and audio_frame is not None:
            # audio
            img, t = audio_frame

    cap.release()
    cv2.destroyAllWindows()


# chidori("Kakashi Raikiri's.mp4")

