import requests
import sys
import json
import re
import requests
from bs4 import BeautifulSoup
from statistics import mean, mode
from collections import Counter
import pandas as pd

# def create_team(team_name: str, team_email: str) -> str:
#     r = requests.post(
#         "https://api.scrapemequickly.com/register",
#         data=json.dumps({"team_name": team_name, "team_email": team_email}),
#         headers={"Content-Type": "application/json"}
#     )

# if r.status_code != 200:
#     print(r.json())
#     print("Failed to create a team")
#     sys.exit(1)

# return r.json()["data"]["team_id"]


def start_scraping_run(team_id: str) -> str:
    r = requests.post(f"https://api.scrapemequickly.com/scraping-run?team_id={"dff0f82d-1241-11f0-8d9a-0242ac120003"}")

    if r.status_code != 200:
        print(r.json())
        print("Failed to start scraping run")
        sys.exit(1)

    return r.json()["data"]["scraping_run_id"]


def submit(answers: dict, scraping_run_id: str) -> bool:
    r = requests.post(
        f"https://api.scrapemequickly.com/cars/solve?scraping_run_id={scraping_run_id}",
        data=json.dumps(answers),
        headers={"Content-Type": "application/json"}
    )

    if r.status_code != 200:
        print(r.json())
        print("Failed to submit answers")
        return False

    return True



base_url = "https://scrapemequickly.com"


# web_doc ='''<html lang="en"><head>
#     <link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;display=swap">
#     <title>Ping Proxies | Scrape Me Quickly</title>
#     <style>
#       body {
#         font-family: "Press Start 2P", cursive;
#       }
       
#       .p-12 {
#         padding: 3rem;
#       }
#       .flex {
#         display: flex;
#       }
#       .justify-center {
#         justify-content: center;
#       }
#       .justify-between {
#         justify-content: space-between;
#       }
#       .items-center {
#         align-items: center;
#       }
#       .min-h-screen {
#         min-height: 100vh;
#       }
#       .bg-[#F2F3F8] {
#         background-color: #f2f3f8;
#       }
#       .text-4xl {
#         font-size: 2.25rem;
#       }
#       .font-bold {
#         font-weight: 700;
#       }
#       .border-2 {
#         border-width: 2px;
#       }
#       .border-[#0D1126] {
#         border-color: #0d1126;
#       }
#       .rounded {
#         border-radius: 0.375rem;
#       }
#       .shadow {
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#       }
#       .shadow-md {
#         box-shadow:
#           0 4px 6px -1px rgba(0, 0, 0, 0.1),
#           0 2px 4px -1px rgba(0, 0, 0, 0.06);
#       }
#       .max-w-2xl {
#         max-width: 42rem;
#       }
#       .w-full {
#         width: 100%;
#       }
#       .h-96 {
#         height: 24rem;
#       }
#       .object-cover {
#         object-fit: cover;
#       }
#       .mt-4 {
#         margin-top: 1rem;
#       }
#       .mt-8 {
#         margin-top: 2rem;
#       }
#       .p-4 {
#         padding: 1rem;
#       }
#       .h-8 {
#         height: 2rem;
#       }
#       .container {
#         width: 100%;
#         margin-left: auto;
#         margin-right: auto;
#         padding-left: 1rem;
#         padding-right: 1rem;
#       }
#       .btn {
#         padding: 0.75rem 1.5rem;
#         background-color: #0d1126;
#         color: white;
#         border-radius: 0.375rem;
#         text-decoration: none;
#         font-size: 1.25rem;
#         font-weight: 600;
#         margin: 0 10px;
#       }
#       .btn:disabled {
#         background-color: #6b7280;
#         cursor: not-allowed;
#       }

       
#       .navbar {
#         background-color: #e5e7f1;
#         padding: 1rem;
#         margin-top: -1rem;
#         margin-left: -1rem;
#         margin-right: -1rem;
#         padding-left: 1rem;
#         padding-right: 1rem;
#         height: 32px;
#       }
#       .navbar-container {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         width: 100%;
#       }

       
#       .text-gray-800 {
#         color: #1f2937;
#       }

#       @media (max-width: 768px) {
#         .md\:hidden {
#           display: block;
#         }
#       }
#       @media (min-width: 769px) {
#         .md\:hidden {
#           display: none;
#         }
#       }
#     </style>
#   </head>
#   <body>
    
#     <nav class="navbar">
#       <div class="container navbar-container">
#         <a href="https://scrapemequickly.com/">
#           <img src="https://ping-proxies-strapi.ams3.digitaloceanspaces.com/public/uploads/ping_logo_b83f7f9c6b.webp" alt="Ping Proxies Logo" class="h-8">
#         </a>
#         <button class="md:hidden text-gray-800"></button>
#       </div>
#     </nav>

#     <div class="p-12 flex justify-center items-center min-h-screen bg-[#F2F3F8]">
#       <div class="p-12 text-[#0D1126] max-w-2xl" id="1" style="border: 2px solid black; border-radius: 0.25rem">
#         <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/VW_T5_PanAmericana_Facelift.JPG/400px-VW_T5_PanAmericana_Facelift.JPG" alt="Volkswagen" class="w-full h-96 object-cover rounded">
#         <h2 class="text-4xl font-bold mt-4 title">Volkswagen, Transporter</h2>
#         <p class="mt-4 text-2xl id"><strong>ID:</strong> 1</p>
#         <p class="mt-4 text-2xl year"><strong>Year:</strong> 2009</p>
#         <p class="mt-4 text-2xl price"><strong>Price:</strong> $22509</p>
#         <p class="text-2xl class"><strong>Class:</strong> Light commercial vehicle</p>
#         <div class="flex justify-center mt-8">
#           <a href="/cars/static/0?scraping_run_id=89d5dca4-0a34-11f0-b686-4a33b21d14f6" class="btn">Prev</a>
#           <a href="/cars/static/2?scraping_run_id=89d5dca4-0a34-11f0-b686-4a33b21d14f6" class="btn ml-4">Next</a>
#         </div>
#       </div>
#     </div>
#     <script>
#       const largeTextStyle =
#         "font-size: 24px; font-weight: bold; color: #A192EC; text-shadow: 1px 1px 2px black;";
#       console.log(
#         "%cEvery webpage has a home; every site has its atlas.",
#         largeTextStyle,
#       );
#     </script>
  

# </body></html>
# '''

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# we need: 
# {
#     "min_year": 1934,
#     "max_year": 2024,
#     "avg_price": 24148,
#     "mode_make": "volkswagen"
# }

url = 'https://scrapemequickly.com/cars/static/0?scraping_run_id=89d5dca4-0a34-11f0-b686-4a33b21d14f6'
data = pd.DataFrame(columns=['make', 'year', 'price'])
for x in range(0, 5):
    try:
        # Step 1: Request the page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser') 
    except:
        print("ERROR1:",soup)
        data.head()
        break
        # Step 2: Extract fields

        #.text Extracts just the inner text (Volkswagen, Transporter)—removes HTML tags.
        #.strip() Removes extra spaces or newlines at the beginning/end.
    try:
        title = soup.find("h2", class_="title").text.strip()
        nextbutton = soup.find("a", class_="btn ml-4")
        if nextbutton:
            relative_url = nextbutton['href']
        print("NEXT BUTTON:",nextbutton)
    except:
        print("ERROR2:",soup)
        break

    try:
        # title.split(","): Splits the title text into a list
        make = title.split(",")[0].strip()  # 'Volkswagen'
        print(make)
        year = int(soup.find("p", class_="year").text.strip().split(":")[1])
        print(year)
        price_text = soup.find("p", class_="price").text.strip()
        print(price_text)
        price = int(re.sub(r'[^\d]', '', price_text))  # Remove $ and commas
        print(price)

        url = base_url + relative_url
        print(url)
        print()
        print()

        datatoappend = {'make': make, 'year': year, 'price': price}
        data = pd.concat([data, pd.DataFrame([datatoappend])], ignore_index=True) # Adds a new row

        if not nextbutton:
            print("FIN")
    except:
        print("ERROR3:",soup)
        break
    
# data processing
data.head()
min_year = data['year'].min()
max_year = data['year'].max()
avg_price = data['price'].mean()
mode_make = data['make'].mode()
print(min_year, max_year, avg_price, mode_make)
data.to_csv('cars.csv', index=False)