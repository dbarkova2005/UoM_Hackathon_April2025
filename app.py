import streamlit as st
import subprocess
import sys
import os
from PIL import Image
from dotenv import load_dotenv

st.write("Python executable being used:")
st.code(sys.executable)


# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("NEUPHONIC_API_KEY")
#client = Neuphonic(api_key=os.getenv('NEUPHONIC_API_KEY'))

# Display title
st.title("Text to Speech Web App")

# Display the image
image_path = "manga_panel\love_is_war8.png"  # change this to your actual image path
image = Image.open(image_path)
st.image(image, caption="Image", use_column_width=True)

# Button to run text_to_speech.py
if st.button("Play Audio"):
    # Run the Python script
    result = subprocess.run(["python", "text_to_speech.py"], capture_output=True, text=True)
    
    # Show output or error
    if result.returncode == 0:
        st.success("Audio played successfully!")
    else:
        st.error("Error occurred while running the script.")
        st.text(result.stderr)
