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
    
    print(invest)



# def analysis(start_date, end_date, avoid):
#     data_open = yf.download(symbols, start=start_date, end=start_date+timedelta(minutes=1))
#     data_close = yf.download(symbols, start=end_date, end=end_date+timedelta(minutes=1))

#     result = {}

#     for ticker in symbols:
#         try:
#             open_price = data_open['Open'][ticker].iloc[0]
#             close_price = data_close['Open'][ticker].iloc[0]
#             result[ticker] = {
#                 'Change %': ((close_price - open_price) / open_price) * 100
#             }
#         except Exception as e:
#             result[ticker] = f"Error: {e}"

#     print(result)
#     return result


import re
import time
from dateparser.search import search_dates
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

def extract_preferences(message: str):
    timer_start = time.time()
    context_dict = {"start_date": None, "end_date": None, "age": -1, "total_budget": None, "avoided_sectors": [], "extraction_time": None}
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
            avoided_sectors = [word for word in avoid_phrase[1:split] if word != ","]
            context_dict["avoided_sectors"] = avoided_sectors
    timer_end = time.time()
    context_dict["extraction_time"] = timer_end-timer_start
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
    ctx = f.readlines()[0]
    msg = eval(ctx)["message"]
    pref = extract_preferences(msg)
# analysis(start_date=pref["start_date"], end_date=pref["end_date"], avoid=pref["avoided_sectors"])
    prices = analysis1(start_date=pref["start_date"], end_date=pref["end_date"], avoid=["crypto"])
