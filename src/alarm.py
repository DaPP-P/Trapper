from pathlib import Path
import time
import datetime
import pygame
import threading


def set_alarm(alarm_time):
    print(f"Alarm set for {alarm_time}")

    sound_file = Path(__file__).parent / "alarm_sound.mp3"

    is_running = True
    alarm_ringing = False

    def listen_for_off():
        nonlocal is_running

        while is_running:
            command = input()

            if command.lower() == "off":
                pygame.mixer.music.stop()
                is_running = False
                print("Alarm turned off.")

    # Start listening for "off"
    threading.Thread(target=listen_for_off, daemon=True).start()

    while is_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)

        if current_time == alarm_time:
            print("AHHHHHHH")

            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()

            alarm_ringing = True

            while pygame.mixer.music.get_busy() and is_running:
                time.sleep(1)

            is_running = False

        time.sleep(1)


if __name__ == "__main__":
    alarm_time = input("Enter the alarm time (HH:MM:SS): ")
    set_alarm(alarm_time)