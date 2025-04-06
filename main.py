import requests
import random
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import threading
import time
# Forgive any dumbass code, blame external conditions e.g. complete sleep deprivation
team_id = "c335f715-12af-11f0-9285-0242ac120003"
MAX_WORKERS = 12
MAX_RETRIES = 3
REQUEST_TIMEOUT = 10

proxies = [
    'http://pingproxies:scrapemequickly@194.87.135.1:9875',
    'http://pingproxies:scrapemequickly@194.87.135.2:9875',
    'http://pingproxies:scrapemequickly@194.87.135.3:9875',
    'http://pingproxies:scrapemequickly@194.87.135.4:9875',
    'http://pingproxies:scrapemequickly@194.87.135.5:9875'
]

# creates a lock object for later 
data_lock = threading.Lock()
token_lock = threading.Lock()
current_token = None

collected_data = []
def get_random_proxy():
    return random.choice(proxies)

def get_token(scraping_run_id):
    url = "https://api.scrapemequickly.com/get-token"
    params = {"scraping_run_id": scraping_run_id}
    headers = {
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-site",
        "Origin": "https://scrapemequickly.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",
    }
    # NO time to wait
    response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
    return response.json()['token']

def fetch_page(scraping_run_id, page_num, token):
    '''
    sends a get rquest to the url which it constructs and the parameters I copied with the token key replaced with what I got,
    all the comments are error checks, etc which I didnt care about in the interest of time, if I had an error I just restarted
    '''
    url = "https://api.scrapemequickly.com/cars/test"
    params = {
        "scraping_run_id": scraping_run_id,
        "per_page": 25,
        "start": 25 * page_num
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            if random.random() < 0.15:  # 15% chance to not use proxy OPTIMAL (i think)
                response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            else:
                response = requests.get(url, headers=headers, params=params, 
                                        proxies={'http': get_random_proxy(), 'https': get_random_proxy()},
                                        timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                return page_num, response.json()['data']
            # necessary for when it inevitably gives: failed to fetch
            elif response.status_code == 401:  # Token expired
                with token_lock:
                    global current_token
                    current_token = get_token(scraping_run_id)
                continue
            elif response.status_code == 429:  # Rate limited
                time.sleep(0.5*attempt)  # as attempts increase, wait longer (theses are necessary dont remove them)
                continue
            else:
                print("Cooked")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for page {page_num}: {str(e)}")
            time.sleep(0.1) # dont remove
    
    return page_num, None

def process_results(data):
    max_year = -float('inf')
    min_year = float('inf')
    total_price = 0
    make_counts = defaultdict(int)
    total_cars = 0
    
    # I honestly have no idea how this doesnt get the correct mean
    # I have tested these functions and they seem to work so my guess is when im 
    # iterating through the data there is an error which potnetially leave off a page causing it or a floating point error ig
    # although idk how this would be, honestly I have no clue, if you can see it please help
    for batch in data:
        for car in batch:
            year = int(car['year'])
            max_year = max(max_year, year)
            min_year = min(min_year, year)
            total_price += car['price']
            make_counts[car['make']] += 1
            total_cars += 1
    
    avg_price = total_price / total_cars
    mode_make = max(make_counts, key=make_counts.get) # if make_counts else None
    
    return {
        "min_year": int(min_year),
        "max_year": int(max_year),
        "avg_price": int(round(avg_price)),
        "mode_make": mode_make
    }

def main(scraping_run_id):
    # gets the token, globalled it to remove UnboundLocalError, I dont know the best practices I am a math student in a hackathon.
    global current_token
    current_token = get_token(scraping_run_id)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # LET THE THREADING BEGIN (chatgpt gave the syntax) - fetch_page going crazy fr
        futures = []
        for page_num in range(1000):
            futures.append(executor.submit(fetch_page, scraping_run_id, page_num, current_token))
        
        # futures allows this to run concurrently as the above is running
        for future in futures:
            page_num, page_data = future.result()
            if page_data:
                with data_lock:
                    # the data lock makes only one thread at a time without it, well there would be like a race condition and I aint implementing a deadlock or hoeer u fix that
                    collected_data.append(page_data)
                print(f"Successfully fetched page {page_num}")
            # else:
            #     print(f"Failed to fetch page {page_num}")
    
    return process_results(collected_data)

def start_scraping_run():
    response = requests.post(
        f"https://api.scrapemequickly.com/scraping-run?team_id={team_id}",
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code != 200:
        print(response.json())
        raise Exception("Failed to start scraping run")
    
    return response.json()["data"]["scraping_run_id"]

def submit(answers, scraping_run_id):
    response = requests.post(
        f"https://api.scrapemequickly.com/cars/solve?scraping_run_id={scraping_run_id}",
        data=json.dumps(answers),
        headers={"Content-Type": "application/json"},
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code != 200:
        print(response.json())
        raise Exception("Failed to submit answers")
    
    return True

if __name__ == "__main__":
    # try:
    scraping_run_id = start_scraping_run()
    print(f"Started scraping run: {scraping_run_id}")
    
    results = main(scraping_run_id)
    print("Processing complete. Results:")
    print(json.dumps(results, indent=2))
    
    if submit(results, scraping_run_id):
        print("Successfully submitted results!")
    # except Exception as e:
        # print(f"Error occurred: {str(e)}")
