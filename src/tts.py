import subprocess

PIPER = "/home/pidaniel/piper/piper"
MODEL = "/home/pidaniel/piper-voices/en_US-lessac-medium.onnx"
OUTPUT = "/tmp/trapper.wav"


def speak(text):
    print(f"Trapper: {text}")

    subprocess.run(
        [
            PIPER,
            "--model",
            MODEL,
            "--output_file",
            OUTPUT,
        ],
        input=text.encode(),
        cwd="/home/pidaniel/piper",
        check=True,
    )

    subprocess.run(
        ["aplay", OUTPUT],
        check=True,
    )
