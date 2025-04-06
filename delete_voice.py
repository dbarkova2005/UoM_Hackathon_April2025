import os
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer
from dotenv import load_dotenv

# Load the API key from the environment
load_dotenv()  # Load variables from .env
client = Neuphonic(api_key=os.getenv('NEUPHONIC_API_KEY'))

# Delete using the voices `voice_id`
response = client.voices.delete(voice_id='fc719704-917e-415c-9048-dd8be1fa8993')

print(response.data)  # display response