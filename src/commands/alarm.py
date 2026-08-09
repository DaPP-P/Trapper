from pathlib import Path
import pygame


alarm_ringing = False


def alarm():
    global alarm_ringing

    sound_file = Path(__file__).parent.parent.parent / "media" / "alarm_sound.mp3"

    print("Alarm is going off.")

    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

    alarm_ringing = True


def turn_off_alarm():
    global alarm_ringing

    alarm_ringing = False

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

    print("Alarm turned off.")
