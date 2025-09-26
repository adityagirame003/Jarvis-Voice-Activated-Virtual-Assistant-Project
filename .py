import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import requests
import musicLibrary

newsapi = "6830730421b14c57adbfefc63ee41eaa"
recognizer = sr.Recognizer()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("http://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("http://linkedin.com")
    elif c.lower().startswith("play"):
        parts = c.lower().split(" ", 1)
        if len(parts) > 1:
            song = parts[1]
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                speak("Sorry, I could not find that song.")
    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )
        if r.status_code == 200:
            articles = r.json().get("articles", [])
            if articles:
                speak("Here are the top headlines.")
                for article in articles[:5]:
                    speak(article["title"])
            else:
                speak("No news found.")
        else:
            speak("Sorry, I could not fetch the news right now.")


if __name__ == "__main__":
    speak("Initializing jarvis...")

    while True:
        try:
            # First listen for wake word
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                print("Wake word detected")
                speak("Yes?")   # <-- jarvis should reply here

                # Now listen for the actual command
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"API Error: {e}")
