from speech import listen
from tts import speak


def handle_command(text):
    text = text.lower()

    if "hello" in text:
        return "Hello. I'm Luna."

    elif "how are you" in text:
        return "I'm doing great. Thanks for asking."

    elif "who are you" in text:
        return "I'm Luna, your personal assistant."

    elif "goodbye" in text:
        return "Goodbye."

    else:
        return "I heard you, but I don't know how to do that yet."


def main():
    speak("Luna is online.")

    while True:
        text = listen()

        response = handle_command(text)

        speak(response)

        if "goodbye" in text:
            break


if __name__ == "__main__":
    main()
