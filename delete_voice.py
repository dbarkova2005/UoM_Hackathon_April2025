import os
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer
from dotenv import load_dotenv

# Load the API key from the environment
load_dotenv()  # Load variables from .env
client = Neuphonic(api_key=os.getenv('NEUPHONIC_API_KEY'))

# Delete using the voices `voice_id`
response = client.voices.delete(voice_id='8fb90d7d-269c-4822-ae7b-01b95200030c')

print(response.data)  # display response