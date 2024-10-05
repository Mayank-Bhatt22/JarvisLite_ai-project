import speech_recognition as sr
import webbrowser
import musicLibrary #your file in which you can store your music in dictionary.
import requests
import os
import google.generativeai as genai # why i used genai because it is free to use
from gtts import gTTS
import pygame
import uuid  # To create unique filenames

recognizer = sr.Recognizer()
newsapi = "YOUR_NEWS_API_KEY"
GeminiAPI = "YOUR_GEMINI_API_KEY"

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

def speak(text):
    # Use gTTS for better audio quality
    unique_filename = f"temp_{uuid.uuid4()}.mp3"  # Create a unique filename
    tts = gTTS(text, lang='en')
    tts.save(unique_filename)

    # Load and play the MP3 file using Pygame
    pygame.mixer.music.load(unique_filename)
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Stop playback before removing the file
    pygame.mixer.music.stop()
    
    # Adding a small delay before removing the file
    pygame.time.delay(50)  # Wait for 50 milliseconds

    # Clean up
    try:
        os.remove(unique_filename)
    except PermissionError as e:
        print(f"Error removing file: {e}")
    
    # Quit the mixer to release resources
    pygame.mixer.quit()
    pygame.mixer.init()  # Re-initialize if needed later

# use of ai
def AIprocess(command):
    GENAI_API_KEY = GeminiAPI
    genai.configure(api_key=GENAI_API_KEY)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 50,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(command)

    return response.text

# to use some of your fav website

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google.")
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        speak("Opening Facebook.")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn.")
        webbrowser.open("https://linkedin.com")

# to open some of your fav songs

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}.")
            webbrowser.open(link)
        else:
            speak("Song not found.")

# to speak news

    elif "news" in c.lower():
        speak("Fetching latest news.")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                speak(articles[0]['title'])
    else:
        output = AIprocess(c)
        speak(output)

# to show you what is going on 

if __name__ == "__main__":
    speak("Jarvis ready.")

    while True:
        r = sr.Recognizer()
        print("Listening...")

        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes?")

                with sr.Microphone() as source:
                    print("Listening for commands...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
# to avoid error 
        except Exception as e:
            print(f"Error: {e}")
