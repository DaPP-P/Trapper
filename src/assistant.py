import datetime

from commands import (
    get_weather,
    alarm,
    turn_off_alarm,
    play,
    pause,
    next_track,
    play_search,
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

    # Start scheduler
    start_scheduler()

    # Preload weather shortly before alarm
    schedule(
        minutes_before(alarm_time, 1),
        preload_weather
    )

    # Set alarm
    schedule(
        alarm_time,
        morning_alarm
    )

    print("Luna is running...")
    print("Alarm set for " + alarm_time)

    speak("Luna is online.")

    # Start voice loop
    while True:

        command = listen()

        response = handle_command(command)

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

    command = command.lower()

    if "weather" in command:
        return get_weather()

    elif "turn off alarm" in command or command == "off":
        turn_off_alarm()
        return f"Good morning {user}."

    elif "play" in command:
        play()
        return "Playing."

    elif "pause" in command:
        pause()
        return "Paused."

    elif "next" in command:
        next_track()
        return "Playing the next track."

    elif "hello" in command:
        return "Hello. I'm Luna."

    elif "who are you" in command:
        return "I'm Luna, your personal assistant."

    else:
        return "I don't know how to do that yet."