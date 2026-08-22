import platform
import subprocess
import ctypes


SYSTEM = platform.system()


# -------------------------
# Windows volume controls
# -------------------------

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

KEYEVENTF_KEYUP = 0x0002


def _press_windows_key(key):
    ctypes.windll.user32.keybd_event(key, 0, 0, 0)
    ctypes.windll.user32.keybd_event(key, 0, KEYEVENTF_KEYUP, 0)


# -------------------------
# Public functions
# -------------------------

def volume_up(steps=2):
    if SYSTEM == "Windows":
        for _ in range(steps):
            _press_windows_key(VK_VOLUME_UP)

    elif SYSTEM == "Linux":
        subprocess.run(
            ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{steps * 5}%+"],
            check=True,
        )


def volume_down(steps=2):
    if SYSTEM == "Windows":
        for _ in range(steps):
            _press_windows_key(VK_VOLUME_DOWN)

    elif SYSTEM == "Linux":
        subprocess.run(
            ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{steps * 5}%-"],
            check=True,
        )


def mute():
    if SYSTEM == "Windows":
        _press_windows_key(VK_VOLUME_MUTE)

    elif SYSTEM == "Linux":
        subprocess.run(
            ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"],
            check=True,
        )