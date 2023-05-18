try:
    import tensorflow  # required in Colab to avoid protobuf compatibility issues
except ImportError:
    pass

import torch
import pyaudio
import wave
import openai
# !pip install ibm_watson
# !pip install ibm_cloud_sdk_core

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# class TextToSpeech:
#
#     def __init__(self, language='en'):
#         self.language = language
#
#     def convert(self, text, filename):
#         tts = gTTS(text=text, lang=self.language)
#         tts.save(filename)
#
#         audio = BytesIO()
#         tts.write_to_fp(audio)
#         # playsound.playsound(tts)
#         # os.system(f"mpg321 {filename}")  # Linux
#         # audio = AudioSegment.from_file(filename, format="mp3")
#         # play(audio)
#         os.system(f"start {filename}")  # Windows
#
#     # def convert(self, text, filename):
#     #     tts = gTTS(text=text, lang=self.language)
#     #     tts.save(filename)
#     #
#     #     with tempfile.NamedTemporaryFile(delete=False) as f:
#     #         tts.write_to_fp(f)
#     #         playsound.playsound(f.name, True)
url = "https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/6c8d7839-f9b7-4682-b61a-9c9a769771e7"
api_key_watson = "xi7gNC6SaIEMWQEReKDmpFny32_ciVb8jLeuSPnxVSmr"
# api_key = "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"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
class TextToSpeech_Watson:
    # Setup Service
    def __init__(self, apikey=api_key_watson):
        openai.api_key = apikey
    # def generate_audio_watson(self, text, apikey = api_key_watson):
        authenticator = IAMAuthenticator(apikey)
        self.tts = TextToSpeechV1(authenticator=authenticator)
        self.tts.set_service_url(url)
    #
    #     with open('output.mp3', 'wb') as audio_file:
    #         res = tts.synthesize(text, accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
    #         audio_file.write(res.content)
    #     playsound.playsound('output.mp3')
    def generate_audio_watson(self, text, apikey = openai.api_key):
        with open('output.wav', 'wb') as audio_file:
            res = self.tts.synthesize(text, accept='audio/wav', voice='en-US_AllisonV3Voice').get_result()
            audio_file.write(res.content)
        self.play_audio_file('output.wav')

    def play_audio_file(self, file_path):
        chunk = 1024
        wf = wave.open(file_path, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()

