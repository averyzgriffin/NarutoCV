import cv2
from ffpyplayer.player import MediaPlayer


folder = "jutsu_videos/"

kakashi = {'name': 'kakashi',
           'Kakashi Sharingan': folder+"Kakashi First Time Using Sharingan.mp4",
           'Ninja Hounds': folder+"",
           'Lightning Blade': folder+"Kakashi Raikiri's.mp4",
           'Hiding': folder+""}

obito = {'name': 'obito',
         'Tobi Chains': folder+"",
         'Tobi Kamui': folder+"",
         'Summoning Nine Tails': folder+"Tobi Nine Tails Full.mp4",
         'Rin': folder+""}

guy = {'name': 'guy',
       'Guy Leaf Whirl Wind':       folder+"",
       'Counter Punch':             folder+"",
       '6th Gate of Joy':           folder+"",
       'Guy Dodge':                 folder+""}

crow = {'name': 'crow',
        'Crow Stab':                  folder+"Crow stab.mp4",
        'Crow Poison Bomb':           folder+"",
        'Crow Black Ant':             folder+"",
        'Crow Substitution':          folder+""}

akamaru = {'name': 'akamaru',
           'Fang over Fang': folder+"",
           'Dynamic Marking': folder+"Inuzuka Kiba Dynamic Air Marking.mp4",
           'Double Headed Wolf': folder+"",
           'Puppy mode': folder+""}

naruto = {'name': 'naruto',
          'Rasengan':           folder+"",
          'Shadow Clone Jutsu': folder+"",
          'Chakra Boost':       folder+"",
          'Shadow Save':        folder+""}


names_of_characters = [kakashi, obito, guy, crow, akamaru, naruto]


def play_video(video):
    cap = cv2.VideoCapture(video)
    video_player = MediaPlayer(video)

    while True:
        audio_frame, val = video_player.get_frame()
        ret, frame = cap.read()

        if not ret:
            break
        if cv2.waitKey(25) & 0xFF == 27:
            break

        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
        cv2.imshow('frame',frame)

    cap.release()
    cv2.destroyAllWindows()

