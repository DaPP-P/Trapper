import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = "models/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

audio_queue = queue.Queue(maxsize=20)


def find_microphone(name="Blue Snowball"):
    devices = sd.query_devices()

    for index, device in enumerate(devices):
        if (
            name.lower() in device["name"].lower()
            and device["max_input_channels"] > 0
        ):
            print(f"Microphone: {device['name']} (device {index})")
            return index

    raise RuntimeError(f"Could not find microphone: {name}")


def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio status: {status}")

    try:
        audio_queue.put_nowait(bytes(indata))
    except queue.Full:
        pass


def listen():
    microphone = find_microphone()

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    print("Listening...")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        device=microphone,
        dtype="int16",
        channels=1,
        callback=audio_callback,
    ):
        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                if text:
                    print(f"You: {text}")
                    return text