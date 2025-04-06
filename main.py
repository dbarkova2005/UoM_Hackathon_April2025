# figure out how to get back admin key via get token
# send the request you get when scrolling to get the test response in json format
# extract da data
team_id = "c335f715-12af-11f0-9285-0242ac120003"
from collections import defaultdict
import requests
import brotli
import zlib
import random
import aiohttp
import asyncio
import sys
import time
import json

MAX_RETRIES = 5
RETRYABLE_CODES = [429, 500, 502, 503, 504, 531]
# Get the token

def process_car_data(cars):
    # Initialize variables for max, min, total price, and mode make count
    max_year = -float('inf')
    min_year = float('inf')
    total_price = 0
    make_counts = defaultdict(int)  # To count occurrences of each make
    
    for car in cars:
        for dict in car:
            year = int(dict['year'])
            max_year = max(max_year, int(year))
            min_year = min(min_year, int(year))

            # Process year
            # print(car['year'])
            
            
            # Process price
            total_price += dict['price']
            
            # Process make (for mode)
            make_counts[dict['make']] += 1

        # Calculate average price
        avg_price = total_price / (len(cars)*25)
        
        # Find mode make (most common make)
    mode_make = max(make_counts, key=make_counts.get)
        
    
    # Return the results
    return max_year, min_year, avg_price, mode_make

def process_car_data(cars):
    max_year = -float('inf')
    min_year = float('inf')
    total_price = 0
    make_counts = defaultdict(int)
    
    for car_batch in cars:  # each batch contains 25 car dictionaries
        for car in car_batch:
            year = int(car['year'])
            max_year = max(max_year, year)
            min_year = min(min_year, year)
            total_price += car['price']
            make_counts[car['make']] += 1

    total_cars = len(cars) * 25
    avg_price = total_price / total_cars
    mode_make = max(make_counts, key=make_counts.get)

    return max_year, min_year, avg_price, mode_make

proxies = ['http://pingproxies:scrapemequickly@194.87.135.1:9875',
'http://pingproxies:scrapemequickly@194.87.135.2:9875',
'http://pingproxies:scrapemequickly@194.87.135.3:9875',
'http://pingproxies:scrapemequickly@194.87.135.4:9875',
'http://pingproxies:scrapemequickly@194.87.135.5:9875']

def get_random_proxy(batch_index):
    if batch_index % 5 == 0:
        time.sleep(0.)
    return {'http': proxies[batch_index % len(proxies)], 'https': proxies[batch_index % len(proxies)]}





# Headers including the Authorization token


def main(scraping_run_idd):
    data = []
    url = "https://api.scrapemequickly.com/get-token"
    params = {
        "scraping_run_id": f"{scraping_run_idd}"
    }
    headerstoken = {
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

    response = requests.get(url, headers=headerstoken, params=params)

    tokendata = response.json()
    token = tokendata['token']
    print("token is: "+ token)
    for x in range(0,1000):
        url = "https://api.scrapemequickly.com/cars/test"
        params = {
            "scraping_run_id": f"{scraping_run_idd}",
            "per_page": 25,
            "start": 25*x
        }

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
        "Priority": "u=1, i"}
        # Send GET request, adds another ip but also some time buffer to allow the stuff to not overload
        if random.randint(0,6) == 6:
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers, params=params, proxies=get_random_proxy(x))
        if x == 0:
            print(response.text)
        if x == 1000:
            print(response.text)

        # Check the response
        
        if response.status_code == 200:
            data.append(response.json()['data'])
            #print("Data:\n", data)
            print(f"Fetched page {x}")
        elif response.status_code == 429:
            print(f"Failed to get data. Status code: {response.status_code}")
            print("Response:", response.json())
            time.sleep(1)
            response = requests.get(url, headers=headers, params=params)
            data.append(response.json()['data'])
            #print("Data:\n", data)

    max_year, min_year, avg_price, mode_make = process_car_data(data)
    print(max_year,min_year,avg_price,mode_make)

    return {
    "min_year": int(min_year),
    "max_year": int(max_year),
    "avg_price": int(round(avg_price)),
    "mode_make": mode_make
}



def start_scraping_run() -> str:
    r = requests.post(f"https://api.scrapemequickly.com/scraping-run?team_id={"c335f715-12af-11f0-9285-0242ac120003"}")
    
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

# Output the results
# print(f"Max Year: {max_year}")
# print(f"Min Year: {min_year}")
# print(f"Average Price: {avg_price:.2f}")
# print(f"Most Common Make: {mode_make}")


scrapingRunID = start_scraping_run()

print(scrapingRunID)
dictin = main(scrapingRunID)
print(dictin)
submit(dictin,scrapingRunID)