import os
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer
from dotenv import load_dotenv

# Load the API key from the environment
load_dotenv()  # Load variables from .env
client = Neuphonic(api_key=os.getenv('NEUPHONIC_API_KEY'))

sse = client.tts.SSEClient()

# TTSConfig is a pydantic model so check out the source code for all valid options
tts_config = TTSConfig(
    speed=1.05,
    lang_code='en', # replace the lang_code with the desired language code.
    voice_id='e564ba7e-aa8d-46a2-96a8-8dffedade48f'  # use client.voices.list() to view all available voices
)

# Create an audio player with `pyaudio`
with AudioPlayer() as player:
    response = sse.send('dasha likes cats', tts_config=tts_config)
    player.play(response)

    player.save_audio('output.wav')  # save the audio to a .wav file