import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

 # Function to listen and recognize speech
def listen():
   with sr.Microphone() as source:
    print("Listening...")
    # Listen for audio (duration in seconds)
    audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Request error: {e}")

listen()