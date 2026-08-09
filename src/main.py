from commands import get_weather, alarm, turn_off_alarm, play, pause, next_track, play_search
from scheduler import schedule, start_scheduler
import datetime


# Updatable
user = "Daniel"
alarm_time = "15:20:00"

weather = None


# Helper Functions
def minutes_before(time_string, minus_minutes):
    alarm_time = datetime.datetime.strptime(time_string, "%H:%M:%S")
    new_time = alarm_time - datetime.timedelta(minutes=minus_minutes)

    return new_time.strftime("%H:%M:%S")

# Programmability

# Method to pull weather data
def preload_weather(location = "Auckland"):
    global weather

    weather = get_weather(location)
    print("Weather preloaded.")

# Method to set the morning Alarm.
def morning_alarm():
    print(weather)
    alarm()


# Calls
start_scheduler()

# Preload Weather data for Alarm
schedule(
    minutes_before(alarm_time, 1),
    preload_weather
)

# Set Alarm
schedule(
    alarm_time,
    morning_alarm
)

print("Trapper is running...")
print("Alarm set for " + alarm_time)


while True:
    command = input("> ")

    if command.lower() == "off":
        turn_off_alarm()
        print("Good Morning", user+".", weather)