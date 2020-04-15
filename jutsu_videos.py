import cv2
from ffpyplayer.player import MediaPlayer


folder = "jutsu_videos/"

kakashi = {'name': 'kakashi',
           'Fire Ball Jutsu': folder+"kakashi fire ball jutsu.mp4",
           'Fanged Pursuit Jutsu': folder+"kakashi fanged pursuit jutsu.mp4",
           'Lightning Blade': folder+"Kakashi Raikiri's.mp4",
           'Water Wall': folder+"kakashi water wall.mp4"}

hiruzen = {'name': 'hiruzen',
         'Tile Shuriken': folder+"Tile Shuriken.mp4",
         'Fire Dragon Flame Bombs': folder+"Hiruzen Fire Dragon Flame Bombs.mp4",
         'Reaper Death Seal': folder+"Reaper Death Seal.mp4",
         'Earth Style Mud Wall': folder+"Hiruzen Earth Style Mud Wall.mp4"}

darui = {'name': 'darui',
       'Darui Water Wall':       folder+"darui water wall.mp4",
       'Emotion Wave':             folder+"Emotion Wave.mp4",
       'Laser Circus':           folder+"Laser Circus.mp4",
       'Sword Defense':                 folder+"Sword Defense.mp4"}

sasuke = {'name': 'sasuke',
        'Fireball Jutsu':                  folder+"Fireball Jutsu.mp4",
        'Dragon Flame Jutsu':           folder+"Dragon Flame Jutsu.mp4",
        'Chidori':             folder+"Chidori.mp4",
        'Sasuke Block':          folder+"Sasuke Block.mp4"}

madara = {'name': 'madara',
           'Majestic Destroyer Flame': folder+"Majestic Destroyer Flame.mp4",
           'Majestic Demolisher': folder+"Majestic Demolisher.mp4",
           'Summoning Nine Tails': folder+"Summoning Nine Tails.mp4",
           'Hiding in Ash': folder+"Hiding in Ash.mp4"}

itachi = {'name': 'itachi',
          'Exploding Clone':           folder+"Exploding Clone.mp4",
          'Shuriken Phoenix Flower': folder+"Shuriken Phoenix Flower.mp4",
          'Grand Fireball Jutsu':       folder+"Grand Fireball Jutsu.mp4",
          'Summoning Crows':        folder+"Summoning Crows.mp4"}


names_of_characters = [kakashi, hiruzen, darui, sasuke, madara, itachi]


def play_video(video):
    cap = cv2.VideoCapture(video)
    video_player = MediaPlayer(video)

    while True:
        audio_frame, val = video_player.get_frame()
        ret, frame = cap.read()

        # h, w, l = frame.shape

        if not ret:
            break
        if cv2.waitKey(25) & 0xFF == 27:
            break

        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
        frame = cv2.resize(frame, (800,600))
        cv2.imshow('frame',frame)

    cap.release()
    cv2.destroyAllWindows()

