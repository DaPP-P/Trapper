import platform
import subprocess
from pathlib import Path
import wave


SYSTEM = platform.system()

# Project root: Trapper/
PROJECT_ROOT = Path(__file__).resolve().parent.parent


if SYSTEM == "Windows":
    PIPER = PROJECT_ROOT / "piper" / "piper.exe"
    MODEL = PROJECT_ROOT / "piper-voices" / "en_US-lessac-medium.onnx"
    OUTPUT = PROJECT_ROOT / "luna-output.wav"

else:
    PIPER = Path("/home/pidaniel/piper/piper")
    MODEL = Path("/home/pidaniel/piper-voices/en_US-lessac-medium.onnx")
    OUTPUT = Path("/tmp/luna-output.wav")

def add_leading_silence(wav_path, silence_seconds=0.5):
    temp_path = str(wav_path) + ".temp.wav"

    with wave.open(str(wav_path), "rb") as source:
        params = source.getparams()
        frames = source.readframes(source.getnframes())

        silence_frames = int(params.framerate * silence_seconds)
        silence = b"\x00" * silence_frames * params.sampwidth * params.nchannels

        with wave.open(temp_path, "wb") as output:
            output.setparams(params)
            output.writeframes(silence + frames)

    Path(temp_path).replace(wav_path)


def speak(text):
    print(f"Luna: {text}")

    subprocess.run(
        [
            str(PIPER),
            "--model",
            str(MODEL),
            "--output_file",
            str(OUTPUT),
        ],
        input=text.encode("utf-8"),
        check=True,
    )

    add_leading_silence(OUTPUT)

    if SYSTEM == "Windows":
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"(New-Object Media.SoundPlayer '{OUTPUT}').PlaySync()"
            ],
            check=True,
        )

    else:
        subprocess.run(
            ["aplay", str(OUTPUT)],
            check=True,
        )