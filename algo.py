import yfinance as yf
# dat = yf.Ticker("MSFT")
# print(dat.info["sector"])
# print(dat.info["industry"])
# print(dat.history(period='1y'))

# var
# age & risk


import re
import time
from dateparser.search import search_dates
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

KEYWORDS = ["finance"]

def pack_portfolio(stock_prices: dict, budget: int):
    portfoio = {}
    remaining_budget = budget
    sorted_stocks = sorted(stock_prices, key=lambda x: stock_prices[x], reverse=True)
    n = len(sorted_stocks)
    while remaining_budget > sorted_stocks[-1]:
        if sorted_stocks[i] <= remaining_budget:
            portfoio[sorted_stocks[i]] = portfoio.get(sorted_stocks[i], 0) + 1
            remaining_budget -= sorted_stocks[i]
            i = (i + 1)%n


def extract_preferences(message: str):
    context_dict = {"start_date": None, "end_date": None, "age": -1, "total_budget": None, "avoided_sectors": [], 
                    # "extraction_time": None
                }
    tokens = word_tokenize(message)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in tokens if
                      word.casefold() not in stop_words]
    context_dict["start_date"] = search_dates(message)[-2][1]
    context_dict["end_date"] = search_dates(message)[-1][1]
    for i, word in enumerate(filtered_words):
        if re.match(r"[0-9]+-year-old", word):
            context_dict["age"] = int(word.split("-")[0])
        elif word == "years":
            context_dict["age"] = int(filtered_words[i-1])
        elif word == "budget":
            budget_phrase = " ".join(filtered_words[i:i+6])
            if "per year" in budget_phrase:
                difference = context_dict["end_date"] - context_dict["start_date"]
                y_diff = (difference.days + difference.seconds/86400)/365.2425
                context_dict["total_budget"] = int(int(budget_phrase.split(" ")[2])*y_diff)
            else:
                context_dict["total_budget"] = int(budget_phrase.split(" ")[2])
        elif word == "total" and filtered_words[i+1] == "investment":
            budget_phrase = filtered_words[i:i+5]
            context_dict["total_budget"] = int(int(budget_phrase[3]))
        elif word == "avoids":
            avoid_phrase = filtered_words[i:]
            split = avoid_phrase.index(".")
            avoided_sectors = [word.lower() for word in avoid_phrase[1:split] if word != ","]
            avoid_list = []
            for kw in KEYWORDS:
                if re.match(kw, " ".join(avoided_sectors)):
                    avoid_list.append(kw)
            context_dict["avoided_sectors"] = avoid_list
    # timer_end = time.time()
    # context_dict["extraction_time"] = timer_end-timer_start
    context_dict["start_date"] = context_dict["start_date"].strftime("%Y-%m-%d")
    context_dict["end_date"] = context_dict["end_date"].strftime("%Y-%m-%d")
    if not any([d == None for d in list(context_dict.values())]):
        return context_dict
    else:
        print("WE CAN'T PARSE: '" + message + "' yet.")
        return False

# count = 0
# total = 0
with open("examples.txt", "r") as f:
    contexts = f.readlines()
    for ctx in contexts:
        msg = eval(ctx)["message"]
        pref = extract_preferences(msg)
        # if pref:
        #     count += 1
        # total += 1
        print(pref)
# print(count/total * 100)