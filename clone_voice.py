import os
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer
from dotenv import load_dotenv

# Load the API key from the environment
load_dotenv()  # Load variables from .env
client = Neuphonic(api_key=os.getenv('NEUPHONIC_API_KEY'))

response = client.voices.clone(
    voice_name='boo',
    voice_file_path='Shirogane.mp3'  # replace with file path to a sample of the voice to clone
)
#C:\Users\Leon Yip Ben Yang\Desktop\UoM_Hackathon_April2025\Shirogane.mp3
print(response.data)  # this will contain a success message with the voice_id of the cloned voice
voice_id = response.data['voice_id']  # store the voice_id for later use