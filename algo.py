import re
import time
from dateparser.search import search_dates
from dateparser import parse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import yfinance as yf
import pandas as pd
import datetime


sectors = ["finance", "technology", "life science", "real estate", "transportation", "energy", "manufacturing"]


symbols = {
    "finance": ["JPM", "BAC", "WFC", "PGR", "GS"],
    "technology": ["AAPL", "MSFT", "NVDA", "GOOG", "AMZN"],
    "life science":["ISRG", "AMGN", "GILD", "VRTX", "REGN", "ALNY"],
    "real estate": ["AMT", "PLD", "PSA", "DLR"],
    "transportation": ["UPS", "UNP", "CSX", "LUV"],
    "energy": ["PAA"],
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
            start_date1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")+datetime.timedelta(days=3)
            end_date1 = datetime.datetime.strptime(end_date, "%Y-%m-%d")+datetime.timedelta(days=3)
            try:
                open_data = yf.download(" ".join(temp_tickers), start=start_date, end=start_date1.strftime("%Y-%m-%d"), progress=False)
                close_data = yf.download(" ".join(temp_tickers), start=end_date, end=end_date1.strftime("%Y-%m-%d"), progress=False)
                # print(open_data)
                # print(close_data)
                if open_data.empty or close_data.empty:
                    continue
                for ticker in open_data['Open']:
                    open_price = open_data['Close'][ticker].iloc[0]
                    close_price = close_data['Open'][ticker].iloc[0]
                    if close_price - open_price > 0:
                        invest[ticker] = float(open_price)
            except Exception as e:
                pass
    
    # print(invest)
    return invest


def pack_portfolio(stock_prices: dict, budget: int):
    portfoio = {}
    remaining_budget = budget*0.5
    stock_prices = list(stock_prices.items())
    sorted_stocks = sorted(stock_prices, key=lambda x: x[1], reverse=True)
    # print(sorted_stocks)
    n = len(sorted_stocks)
    i = 0
    while remaining_budget > sorted_stocks[-1][1]: 
        if sorted_stocks[i][1] <= remaining_budget:
            portfoio[sorted_stocks[i][0]] = portfoio.get(sorted_stocks[i][0], 0) + 1
            remaining_budget -= sorted_stocks[i][1]
        i = (i + 1)%n
    # print(remaining_budget)
    return portfoio

def extract_preferences(message: str):
    context_dict = {"start_date": None, "end_date": None, "age": -1, "total_budget": None, "avoided_sectors": [], 
                    # "extraction_time": None
                }
    tokens = word_tokenize(message)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in tokens if
                      word.casefold() not in stop_words]
    start_index = " ".join(filtered_words).find("start")
    dates = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", " ".join(filtered_words)[start_index:])
    if len(dates) != 2:
        try:
            dates = [d[1] for d in search_dates(" ".join(filtered_words)[start_index:]) if 2000 < d[1].year < 2026]
        except IndexError:
            # print(filtered_words)
            return False
        if len(dates) != 2:
            # print(filtered_words)
            return False
        context_dict["start_date"] = dates[0]
        context_dict["end_date"] = dates[1]
    else:
        context_dict["start_date"] = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
        context_dict["end_date"] = datetime.datetime.strptime(dates[1], "%Y-%m-%d")
    for i, word in enumerate(filtered_words):
        if re.match(r"[0-9]+-year-old", word):
            context_dict["age"] = int(word.split("-")[0])
        elif word == "years":
            context_dict["age"] = int(filtered_words[i-1])
            if int(filtered_words[i-1]) > 50:
                # print(context_dict)
                return False
        elif word == "budget":
            budget_phrase = " ".join(filtered_words[i:i+6])
            budget_val = int([b for b in word_tokenize(budget_phrase) if b.isnumeric()][0])
            print(budget_val)
            if "per year" in budget_phrase:
                difference = context_dict["end_date"] - context_dict["start_date"]
                y_diff = (difference.days + difference.seconds/86400)/365.2425
                context_dict["total_budget"] = int(budget_val*y_diff)
            else:
                context_dict["total_budget"] = budget_val
        elif word == "total" and filtered_words[i+1] == "investment":
            if "budget" in filtered_words:
                return False
            budget_phrase = filtered_words[i:i+5]
            context_dict["total_budget"] = int(int(budget_phrase[3]))
        elif word == "avoids" or word == "avoid":
            avoid_phrase = filtered_words[i:]
            split = avoid_phrase.index(".")
            avoided_sectors = [word.lower() for word in avoid_phrase[1:split] if word != ","]
            # print(avoided_sectors)
            avoid_list = []
            for kw in sectors:
                if re.search(kw, " ".join(avoided_sectors)):
                    avoid_list.append(kw)
            context_dict["avoided_sectors"] = avoid_list
    # timer_end = time.time()
    # context_dict["extraction_time"] = timer_end-timer_start
    # print(context_dict["start_date"])
    context_dict["start_date"] = context_dict["start_date"].strftime("%Y-%m-%d")
    context_dict["end_date"] = context_dict["end_date"].strftime("%Y-%m-%d")
    if not any([d == None for d in list(context_dict.values())]):
        # print(context_dict)
        return context_dict
    else:
        # print("WE CAN'T PARSE: '" + message + "' yet.")
        # print(context_dict)
        return False
    
# print(extract_preferences("Andre Webb is 19 years old, he started investing in 2012-04-11, and his investment end date was 2013-10-08. He enjoys hiking, and he avoids structured finance, life sciences, and finance. He has a true salary of $204,950 per year, and a budget of $10570."))

def compute(message: str):
    pref = extract_preferences(message)
    if (pref):
        prices = analysis1(start_date=pref["start_date"], end_date=pref["end_date"], avoid=pref["avoided_sectors"])
        portfolio_dict = pack_portfolio(prices, pref["total_budget"])
        return list(portfolio_dict.items())
    else:
        return None
    
def calculate_risk(std_matrix):
    pass

# print(compute("Lisa Welch is 27 years old and has a total budget of $17669. Her investment start date is 2017-05-14 and her investment end date is 2018-06-04. Her hobbies are learning languages and she avoids life sciences, finance, and crypto."))

# 
# with open("examples.txt", "r") as f:
#     with open("output.txt", "a") as g:
#         ctxs = f.readlines()
#         for ctx in ctxs:
#             msg = eval(ctx)["message"]
#             pref = extract_preferences(msg)
#             prices = analysis1(start_date=pref["start_date"], end_date=pref["end_date"], avoid=pref["avoided_sectors"])
#             g.write(str(pack_portfolio(prices, pref["total_budget"])) + "\n")
