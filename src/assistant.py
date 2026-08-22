import datetime

from commands import (
    get_weather,
    alarm,
    turn_off_alarm,
    play,
    pause,
    next_track,
    play_search,
    volume_up,
    volume_down,
    mute
)

from scheduler import schedule, start_scheduler

from speech import listen
from tts import speak


# Settings

user = "Daniel"
alarm_time = "15:20:00"

weather = None


# Helper Functions

def minutes_before(time_string, minus_minutes):
    alarm_time = datetime.datetime.strptime(time_string, "%H:%M:%S")
    new_time = alarm_time - datetime.timedelta(minutes=minus_minutes)

    return new_time.strftime("%H:%M:%S")


# Setup Functions
def start_luna():
    start_scheduler()

    schedule(
        minutes_before(alarm_time, 1),
        preload_weather
    )

    schedule(
        alarm_time,
        morning_alarm
    )

    print("Luna is running...")
    print("Say 'Luna' to wake me.")

    while True:
        command = listen().lower().strip()

        # Luna wasn't mentioned
        if "luna" not in command:
            print("Wake word not detected. Ignoring.")
            continue

        # Take everything AFTER "luna"
        command = command.split("luna", 1)[1].strip()

        # They only said "Luna", "Hey Luna", etc.
        if not command:
            speak("Yes?")
            command = listen().lower().strip()

        response = handle_command(command)

        if response:
            speak(response)


# Commands

def preload_weather(location="Auckland"):
    global weather

    weather = get_weather(location)

    print("Weather preloaded.")


def morning_alarm():
    print(weather)
    alarm()


# Voice command handling
def handle_command(command):
    command = command.lower().strip()

    if "weather" in command:
        return get_weather("Auckland")

    elif "turn off alarm" in command or command == "off":
        turn_off_alarm()
        return f"Good morning {user}."

    # "play Everlong", "play Mr Brightside", etc.
    elif command.startswith("play "):
        search = command.removeprefix("play ").strip()
        song = play_search(search)

        if song:
            return f"Playing {song}."

        return f"I couldn't find {search}."

    # Just "play" resumes Spotify
    elif command == "play":
        song = play()

        if song:
            return f"Playing {song}."

        return "Playing Spotify."

    elif "pause" in command:
        pause()
        return "Paused Spotify."

    elif "next" in command:
        next_track()
        return "Playing the next track."

    elif "hello" in command:
        return "Hello. I'm Luna."

    elif "who are you" in command:
        return "I'm Luna, your personal assistant."
    
    elif "volume up" in command or "turn it up" in command:
        volume_up()
        return "Volume up."

    elif "volume down" in command or "turn it down" in command:
        volume_down()
        return "Volume down."

    elif "mute" in command:
        mute()
        return None

    else:
        return "I don't know how to do that yet."