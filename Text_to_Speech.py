# from gtts import gTTS
# import os
# from io import BytesIO
import playsound
# import tempfile
# from pydub import AudioSegment
# from pydub.playback import play
import requests
import json
try:
    import tensorflow  # required in Colab to avoid protobuf compatibility issues
except ImportError:
    pass

import torch
import pandas as pd
# import whisper
import torchaudio

from tqdm.notebook import tqdm
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
api_key = "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"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
class TextToSpeech_Watson:
    # Setup Service
    def __init__(self, apikey=api_key_watson):
        openai.api_key = apikey
    def generate_audio_watson(self, text, apikey = api_key_watson):
        authenticator = IAMAuthenticator(apikey)
        tts = TextToSpeechV1(authenticator=authenticator)
        tts.set_service_url(url)

        with open('./speech.mp3', 'wb') as audio_file:
            res = tts.synthesize(text, accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
            audio_file.write(res.content)
        playsound.playsound('./speech.mp3')

# class TextToSpeech:
#     import openai
#
#
#     def __init__(self, api_key="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"):
#         openai.api_key = api_key
#
#     def generate_audio(self, input_text, voice="text-to-speech/whisper-1"):
#         filename = "output.wav"
#         response = openai.Completion.create(
#             engine="text-davinci-002",
#             prompt=(
#                 f"Please generate an audio clip of the following text:\n\n{input_text}\n\n"
#                 f"using the {voice} voice"
#             ),
#             max_tokens=1024,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
#         audio_url = response.choices[0].text.strip()
#         choices = response.choices[0]
#         print(dir(choices))
#         try:
#             audio_bytes = choices.audio
#             with open(filename, "wb") as f:
#                 f.write(audio_bytes)
#         except AttributeError:
#             raise ValueError("The 'audio' attribute is not available in the API response")
#
#
#         os.system(f"start {filename}")  # Windows
#         playsound.playsound(filename)


# class TextToSpeech_Vall_E:
#     def __init__(self, api_key):
#         openai.api_key = api_key
#
#     # def generate_audio(self, text, voice):
#     #     model_engine = "text-davinci-002"
#     #     image_size = 256
#     #
#     #     # Encode the text using DALL-E 2 API
#     #     response = openai.Completion.create(
#     #         engine=model_engine,
#     #         prompt=f"Convert this text to an image of size {image_size}x{image_size} and read it out loud: {text}",
#     #         temperature=0.7,
#     #         max_tokens=1024,
#     #         n=1,
#     #         stop=None,
#     #     )
#     #
#     #     # Extract the image URL from the response
#     #     image_url = response.choices[0].text.strip()
#     #
#     #     # Download the image
#     #     headers = {
#     #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
#     #     response = requests.get(image_url, headers=headers)
#     #     if response.status_code != 200:
#     #         raise ValueError(f"Failed to fetch image with status code: {response.status_code}")
#     #
#     #     # Convert the image to base64 encoded string
#     #     image_b64 = response.content.hex()
#     #
#     #     # Synthesize speech from the image using Voice model
#     #     response = openai.api_request("vall-e-beta/decode", {
#     #         "model": f"image-alpha-001/{voice}",
#     #         "image": image_b64,
#     #     })
#     #
#     #     # Extract the audio URL from the response
#     #     audio_url = response['responses'][0]['decodings'][0]['audio_url']
#     #
#     #     # Download the audio file
#     #     response = requests.get(audio_url, headers=headers)
#     #     if response.status_code != 200:
#     #         raise ValueError(f"Failed to fetch audio with status code: {response.status_code}")
#     #
#     #     # Save the audio to file and play it
#     #     filename = "output.mp3"
#     #     with open(filename, 'wb') as f:
#     #         f.write(response.content)
#     #
#     #     # Play the audio file using system command
#     #     import os
#     #     os.system(f"start {filename}")  # Windows
#     def generate_audio(self, input_text, voice="vall-e", _api_key=api_key, _base_url="https://api.vall-e.com"):
#         # Create the API endpoint URL
#         url = "https://api.vall-e.com" + "/tts"
#
#         # Set the request headers
#         headers = {
#             "Authorization": f"Bearer {api_key}",
#             "Content-Type": "application/json"
#         }
#
#         # Set the request data
#         data = {
#             "text": input_text,
#             "voice": voice
#         }
#
#         # Send the API request
#         response = requests.post(url, headers=headers, json=data, verify=False)
#
#         # Check for errors
#         if response.status_code != 200:
#             print(f"Error generating audio: {response.status_code} - {response.text}")
#             return None
#
#         # Get the audio content
#         audio_content = response.content
#
#         # Save the audio to a file
#         with open("output.wav", "wb") as f:
#             f.write(audio_content)
#
#         # Play the audio
#         playsound.playsound("output.wav")

# import os
# tts = TextToSpeech_Vall_E(api_key)
# tts.generate_audio("Hello, how are you?", voice="vall-e")