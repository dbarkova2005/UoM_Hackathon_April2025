import re
import time
from dateparser.search import search_dates
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import yfinance as yf
import pandas as pd
import datetime


sectors = ["crypto", "finance", "technology", "life science", "real estate", "transportation", "energy", "manufacturing"]


symbols = {
    "crypto": ["BTC", "ETH", "XRP", "BNB", "USDT"],
    "finance": ["JPM", "BAC", "WFC", "PGR", "GS", "SPGI"],
    "technology": ["AAPL", "MSFT", "NVDA", "GOOG", "GOOGL", "META", "AMZN"],
    "life science":["ISRG", "AMGN", "GILD", "VRTX", "REGN", "ALNY"],
    "real estate": ["AMT", "WELL", "PLD", "PSA", "DLR", "VICI"],
    "transportation": ["UPS", "DAL", "UNP", "CSX", "LUV", "UBER"],
    "energy": ["FANG", "EXE", "EXEEW", "VNOM", "EXEEL", "PAA"],
    "manufacturing": ["MMM", "CAT", "DE", "AMAT", "GE", "HON"]
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

def analysis1(start_date, end_date, avoid):

    invest = {}
    for sector in sectors:
        if sector in avoid:
            continue
        else:
            temp_tickers = symbols[sector]
            # for ticker in temp_tickers:
            start_date1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")+datetime.timedelta(days=1)
            end_date1 = datetime.datetime.strptime(end_date, "%Y-%m-%d")+datetime.timedelta(days=1)
            try:
                open_data = yf.download(" ".join(temp_tickers), start=start_date, end=start_date1.strftime("%Y-%m-%d"))
                close_data = yf.download(" ".join(temp_tickers), start=end_date, end=end_date1.strftime("%Y-%m-%d"))
                print(open_data)
                print(close_data)
                for ticker in open_data['Open']:
                    open_price = open_data['Open'][ticker].iloc[0]
                    close_price = close_data['Open'][ticker].iloc[0]
                    if close_price - open_price > 0:
                        invest[ticker] = float(open_price)
            except Exception as e:
                pass
    
    # print(invest)
    return invest


def pack_portfolio(stock_prices: dict, budget: int):
    portfoio = {}
    remaining_budget = budget
    stock_prices = list(stock_prices.items())
    sorted_stocks = sorted(stock_prices, key=lambda x: x[1], reverse=True)
    print(sorted_stocks)
    n = len(sorted_stocks)
    i = 0
    while remaining_budget > sorted_stocks[-1][1]:
        if sorted_stocks[i][1] <= remaining_budget:
            portfoio[sorted_stocks[i][0]] = portfoio.get(sorted_stocks[i][0], 0) + 1
            remaining_budget -= sorted_stocks[i][1]
        i = (i + 1)%n
    return portfoio

def extract_preferences(message: str):
    context_dict = {"start_date": None, "end_date": None, "age": -1, "total_budget": None, "avoided_sectors": [], 
                    # "extraction_time": None
                }
    tokens = word_tokenize(message)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in tokens if
                      word.casefold() not in stop_words]
    context_dict["start_date"] = search_dates(message)[0][1]
    context_dict["end_date"] = search_dates(message)[1][1]
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
            print(" ".join(avoided_sectors))
            for kw in sectors:
                if re.search(kw, " ".join(avoided_sectors)):
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

def compute(message: str):
    pref = extract_preferences(message)
    print(pref)
    prices = analysis1(start_date=pref["start_date"], end_date=pref["end_date"], avoid=pref["avoided_sectors"])
    print(prices)
    return pack_portfolio(prices, pref["total_budget"])

print(compute("Christopher Avila is a 67-year-old investor who started investing in 2011-07-01 and ended it on 2014-06-11. His hobbies include learning languages, and he avoids finance or crypto assets. He has a total budget of $23215."))
# count = 0
# total = 0
# with open("examples.txt", "r") as f:
#     ctx = f.readlines()[0]
#     msg = eval(ctx)["message"]
#     pref = extract_preferences(msg)
#     prices = analysis1(start_date=pref["start_date"], end_date=pref["end_date"], avoid=pref["avoided_sectors"])
#     print(pack_portfolio(prices, pref["total_budget"]))
