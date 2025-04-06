# figure out how to get back admin key via get token
# send the request you get when scrolling to get the test response in json format
# extract da data

from collections import defaultdict
import requests
import brotli
import zlib
import random
import aiohttp
import asyncio
import sys
# Step 1: Get the token

def process_car_data(cars):
    # Initialize variables for max, min, total price, and mode make count
    max_year = -float('inf')
    min_year = float('inf')
    total_price = 0
    make_counts = defaultdict(int)  # To count occurrences of each make
    
    for car in cars:
        # Process year
        # print(car['year'])
        year = int(car['year'])
        max_year = max(max_year, int(year))
        min_year = min(min_year, int(year))
        
        # Process price
        total_price += car['price']
        
        # Process make (for mode)
        make_counts[car['make']] += 1

    # Calculate average price
    avg_price = total_price / len(cars)
    
    # Find mode make (most common make)
    mode_make = max(make_counts, key=make_counts.get)
    
    # Return the results
    return max_year, min_year, avg_price, mode_make

proxies = ['http://pingproxies:scrapemequickly@194.87.135.1:9875',
'http://pingproxies:scrapemequickly@194.87.135.2:9875',
'http://pingproxies:scrapemequickly@194.87.135.3:9875',
'http://pingproxies:scrapemequickly@194.87.135.4:9875',
'http://pingproxies:scrapemequickly@194.87.135.5:9875']

def get_random_proxy(batch_index):
    return {'http': proxies[batch_index % len(proxies)], 'https': proxies[batch_index % len(proxies)]}

url = "https://api.scrapemequickly.com/cars/test"
params = {
    "scraping_run_id": "89d5dca4-0a34-11f0-b686-4a33b21d14f6"
}
headers = {
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-site",
    "Origin": "https://scrapemequickly.com",
    "Sec-Fetch-Dest": "empty",
    "Accept-Language": "en-GB,en;q=0.9",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://scrapemequickly.com/",
    "Priority": "u=3, i"
}

response = requests.get(url, headers=headers, params=params)

tokendata = response.json()
token = tokendata['token']

# URL for the actual GET request
url = "https://api.scrapemequickly.com/cars/test"

# Headers including the Authorization token
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "*/*",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Dest": "empty",
    "Origin": "https://scrapemequickly.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Referer": "https://scrapemequickly.com/",
    "Priority": "u=1, i"
}
async def fetch_data(session, url, headers, params):
    async with session.get(url, headers=headers, params=params) as response:
        return await response.json()

async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for x in range(1, 4000):
            params = {
                "scraping_run_id": "89d5dca4-0a34-11f0-b686-4a33b21d14f6",
                "per_page": 25,
                "start": 25 * x
            }
            tasks.append(fetch_data(session, url, headers, params))
        results = await asyncio.gather(*tasks)
        # Process results here
        return results

data = asyncio.run(main())



max_year, min_year, avg_price, mode_make = process_car_data(data)

def start_scraping_run(team_id: str) -> str:
    r = requests.post(f"https://api.scrapemequickly.com/scraping-run?team_id={"dff0f82d-1241-11f0-8d9a-0242ac120003"}")
    
    if r.status_code != 200:
        print(r.json())
        print("Failed to start scraping run")
        sys.exit(1)

    return r.json()["data"]["scraping_run_id"]

# Output the results
print(f"Max Year: {max_year}")
print(f"Min Year: {min_year}")
print(f"Average Price: {avg_price:.2f}")
print(f"Most Common Make: {mode_make}")