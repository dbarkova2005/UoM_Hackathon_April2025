import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://www.webnovel.com/book/classroom-of-the-elite-year-1_24347597906049405/prologue-the-structure-of-japanese-society_65357609691053336"

# Send a GET request
response = requests.get(url)
response.raise_for_status()  # Check for HTTP errors

# Parse HTML and extract text
soup = BeautifulSoup(response.text, 'html.parser')

# Remove scripts/styles and get clean text
text = soup.get_text(separator=' ', strip=True)

# Print the first 500 characters (avoid overwhelming output)
print(text[:500])