import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import webbrowser
import ctypes
import subprocess
import sys


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

#Speech Recognition
listener = sr.Recognizer()

def listen_command():
    """Listen for a voice command and return it as lowercase text."""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = listener.listen(source)
            command = listener.recognize_google(audio).lower()
            if "voice assistant" in command:
                command = command.replace("voice assistant", "").strip()
            print(f"Command: {command}")
            return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f" Could not request results; {e}")
        return ""


def process_command(command):
    """Process the given voice command."""
    if not command:
        speak("Please repeat, I did not understand")
        return

    if "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif "what is time now" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Current time is {time_now}")

    elif "what is date" in command:
        today = datetime.datetime.now().strftime("%d/%m/%Y")
        speak(f"Today's date is {today}")

    elif "how r u" in command:
        speak("I am fine, how about you?")

    elif "what is your name" in command:
        speak("I am your voice assistant. What can I do for you?")

    elif "who is" in command:
        person = command.replace("who is", "").strip()
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            speak(info)
        except wikipedia.exceptions.DisambiguationError:
            speak("Please be more specific, there are multiple matches.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I could not find any information.")

    elif "say joke" in command:
        speak(pyjokes.get_joke())

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "change background" in command:
        ctypes.windll.user32.SystemParametersInfoW(
            20, 0,
            r"E:\wallpaperflare.com_wallpaper (8).jpg", 0
        )
        speak("Background changed successfully")

    elif "lock window" in command:
        speak("Locking the device")
        ctypes.windll.user32.LockWorkStation()

    elif "shutdown system" in command:
        speak("Shutting down the system")
        subprocess.call('shutdown /p /f')

    else:
        speak("Please repeat, I did not understand")


def main():
    try:
        command = listen_command()
        process_command(command)
    finally:
        try:
            engine.stop()
        except Exception:
            pass  
        if 'pyttsx3' in sys.modules:
            del sys.modules['pyttsx3']


if __name__ == "__main__":
    main()
