import os
import json
#import read_manga_panel
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer
from dotenv import load_dotenv
from test import get_output_of_panel


# Load the API key from the environment
load_dotenv()  # Load variables from .env
client = Neuphonic(api_key=os.getenv('NEUPHONIC_API_KEY'))

sse = client.tts.SSEClient()



#with open("my_data.json", "r") as file:
#    data = json.load(file) # data is a dictionary


# put this in a for loop

# TTSConfig is a pydantic model so check out the source code for all valid options
#x = 1
# default english dude
#if x == 0:
#    tts_config = TTSConfig(
#        speed=1,
#        lang_code='en', # replace the lang_code with the desired language code.
#        voice_id='e564ba7e-aa8d-46a2-96a8-8dffedade48f'  # use client.voices.list() to view all available voices
#    )
# kaguya (dub)
#elif x == 1:
#    tts_config = TTSConfig(
#        speed=1,
#        lang_code='en', # replace the lang_code with the desired language code.
#        voice_id='fc719704-917e-415c-9048-dd8be1fa8993'  # use client.voices.list() to view all available voices
#    )
# shirograne (sub)
#elif x == 2:
#    tts_config = TTSConfig(
#        speed=1,
#        lang_code='en', # replace the lang_code with the desired language code.
#        voice_id='af4f20d8-1392-45e0-884e-7740713f3763'  # use client.voices.list() to view all available voices
#    )

# kaguya - dub: fc719704-917e-415c-9048-dd8be1fa8993
#default: e564ba7e-aa8d-46a2-96a8-8dffedade48f
# shirogane: af4f20d8-1392-45e0-884e-7740713f3763
#b19687fd-c5c9-4bda-9d52-756c3b10c88e
#print(client.voices.list())

#print(ray)
#print(data)
dialogue = get_output_of_panel()

# Create an audio player with `pyaudio`

# iterate through the dialogue array 
# if dialogue[i][0] == 'KAGUYA' -> turn AI model into speech fro her voice
for i in range(0, len(dialogue)):
    if dialogue[i][0] == 'KAGUYA':
        #kaguya
        tts_config = TTSConfig(
            speed=1,
            lang_code='en', # replace the lang_code with the desired language code.
            voice_id='99000bca-6657-4d7e-a9c2-f67f478825f8'  # use client.voices.list() to view all available voices
        )
                
        with AudioPlayer() as player:
            response = sse.send(dialogue[i][1], tts_config=tts_config)
            player.play(response)

    elif dialogue[i][0] == 'SHIROGANE':

        tts_config = TTSConfig(
            speed=1,
            lang_code='en', # replace the lang_code with the desired language code.
            voice_id='af4f20d8-1392-45e0-884e-7740713f3763'  # use client.voices.list() to view all available voices
        )

        with AudioPlayer() as player:
            response = sse.send(dialogue[i][1], tts_config=tts_config)
            player.play(response)

    #player.save_audio('output.wav')  # save the audio to a .wav file