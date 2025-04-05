import cv2
import numpy as np
import easyocr  # Replaced pytesseract with easyocr

# Initialize EasyOCR reader (English only, CPU mode)
reader = easyocr.Reader(['en'], gpu=False)  # Add more languages like ['en','ja'] if needed

# Load and preprocess the image (your existing steps)
image = cv2.imread("manga_panel\love_is_war4.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV, 21, 10
)
denoised = cv2.fastNlMeansDenoising(thresh, h=7)
scaled = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Save preprocessed image for EasyOCR (optional but recommended)
cv2.imwrite("preprocessed_easyocr.png", scaled)

# Extract text with EasyOCR (replacing pytesseract)
result = reader.readtext(
    "preprocessed_easyocr.png",  # Or pass the numpy array directly: scaled
    detail=0,                    # Return text only
    paragraph=True,              # Group text logically
    text_threshold=0.7           # Adjust if needed (0-1)
)

# Print cleaned output
print("Extracted Text:")
print("\n".join(result))  # Preserves original line breaks