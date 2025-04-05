import os
#import clone_voice.py
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer
from dotenv import load_dotenv

# Load the API key from the environment
load_dotenv()  # Load variables from .env
client = Neuphonic(api_key=os.getenv('NEUPHONIC_API_KEY'))

sse = client.tts.SSEClient()

# TTSConfig is a pydantic model so check out the source code for all valid options
x = 1
# default english dude
if x == 0:
    tts_config = TTSConfig(
        speed=1,
        lang_code='en', # replace the lang_code with the desired language code.
        voice_id='e564ba7e-aa8d-46a2-96a8-8dffedade48f'  # use client.voices.list() to view all available voices
    )
# kaguya (dub)
elif x == 1:
    tts_config = TTSConfig(
        speed=1,
        lang_code='en', # replace the lang_code with the desired language code.
        voice_id='fc719704-917e-415c-9048-dd8be1fa8993'  # use client.voices.list() to view all available voices
    )
# shirograne (sub)
elif x == 2:
    tts_config = TTSConfig(
        speed=1,
        lang_code='en', # replace the lang_code with the desired language code.
        voice_id='af4f20d8-1392-45e0-884e-7740713f3763'  # use client.voices.list() to view all available voices
    )

# kaguya - dub: fc719704-917e-415c-9048-dd8be1fa8993
#default: e564ba7e-aa8d-46a2-96a8-8dffedade48f
# shirogane: af4f20d8-1392-45e0-884e-7740713f3763
#b19687fd-c5c9-4bda-9d52-756c3b10c88e
#print(client.voices.list())

# Create an audio player with `pyaudio`
with AudioPlayer() as player:
    response = sse.send('cat cat cat cat', tts_config=tts_config)
    player.play(response)

    player.save_audio('output.wav')  # save the audio to a .wav file