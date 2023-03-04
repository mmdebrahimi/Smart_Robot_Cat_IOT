import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_speech(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Speak now...")
            audio_data = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio_data)
            # create a SpeechRecognizer object

            return text







