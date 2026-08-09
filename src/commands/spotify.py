import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPE = "user-modify-playback-state user-read-playback-state"

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE
    )
)

def show_devices():
    devices = spotify.devices()

    for device in devices["devices"]:
        print(
            device["name"],
            "-",
            device["type"],
            "-",
            device["id"]
        )

def play(device_name="DESKTOP-COUG4J8"):
    devices = spotify.devices()["devices"]

    device = next(
        (device for device in devices if device["name"] == device_name),
        None
    )

    if device is None:
        print(f"{device_name} is not available.")
        return

    spotify.start_playback(device_id=device["id"])

    print(f"Playing on {device['name']}")
    

def pause():
    spotify.pause_playback()


def next_track():
    spotify.next_track()


def previous_track():
    spotify.previous_track()


def play_search(search):
    devices = spotify.devices()["devices"]

    if not devices:
        print("No Spotify devices available.")
        return

    device_name = "DESKTOP-COUG4J8"

    device = next(
        (device for device in devices if device["name"] == device_name),
        None
    )

    if device is None:
        print(f"{device_name} is not available.")
        return

    results = spotify.search(
        q=search,
        type="track",
        limit=1
    )

    tracks = results["tracks"]["items"]

    if not tracks:
        print(f"I couldn't find {search} on Spotify.")
        return

    track = tracks[0]

    spotify.start_playback(
        device_id=device["id"],
        uris=[track["uri"]]
    )

    print(
        f"Playing {track['name']} by "
        f"{track['artists'][0]['name']}"
    )
