import yfinance as yf
import pandas as pd

symbols = [
    "PLTR", "MSTR", "AXON", "APP", "ARM", "LIN", "AZN", "BKR", "AVGO", "BIIB",
    "BKNG", "CDNS", "ADBE", "CHTR", "CPRT", "CSGP", "CRWD", "CTAS", "CSCO", "CMCSA",
    "COST", "CSX", "CTSH", "DDOG", "DXCM", "FANG", "EA", "ON", "EXC", "TTD", "FAST",
    "GFS", "META", "FI", "FTNT", "GILD", "GOOG", "GOOGL", "HON", "INTC", "INTU", "ISRG",
    "MRVL", "IDXX", "KDP", "KLAC", "KHC", "LRCX", "LULU", "MELI", "MAR", "MCHP", "MDLZ",
    "MNST", "MSFT", "MU", "NFLX", "GRAL", "NVDA", "NXPI", "ODFL", "ORLY", "PCAR", "PANW",
    "PAYX", "PDD", "PYPL", "PEP", "QCOM", "REGN", "ROST", "SBUX", "SNPS", "TSLA", "TXN",
    "TMUS", "VRSK", "VRTX", "WBD", "WDAY", "XEL", "ZS", "ADP", "ABNB", "AMD", "CEG", "AMZN",
    "AMGN", "AEP", "CDW", "CCEP", "ADI", "MDB", "DASH", "ROP", "ANSS", "AAPL", "AMAT", "GEHC",
    "ASML", "TEAM", "ADSK"
]

def test_yfinance():
    temp = ""
    # print(dat.info["sector"])
    # print(dat.info["industry"])
    # print(dat.history(period='1y'))

    for ticker in symbols:
        temp = yf.Ticker(ticker)


def analysis(start_date, end_date, avoid):
    data = yf.download(symbols, start="2023-04-14", end="2024-12-14")

    result = {}

    for ticker in symbols:
        try:
            open_price = data['Open'][ticker].iloc[0]
            close_price = data['Close'][ticker].iloc[-1]
            result[ticker] = {
                'Change %': ((close_price - open_price) / open_price) * 100
            }
        except Exception as e:
            result[ticker] = f"Error: {e}"

    print(result)
    return result


import re
from dateparser import parse as date_parse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
def extract_preferences(message: str):
    context_dict = {"start_date": None, "end_date": None, "age": None}
    tokens = word_tokenize(message)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in tokens if
                      word.casefold() not in stop_words]
    for i, word in enumerate(filtered_words):
        if re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", word):
            if context_dict["start_date"] == None:
                context_dict["start_date"] = date_parse(word).strftime("%Y-%m-%d")
            else:
                context_dict["end_date"] =  date_parse(word).strftime("%Y-%m-%d")
        elif word in MONTHS:
            date = " ".join(filtered_words[i:i+4])
            if context_dict["start_date"] == None:
                context_dict["start_date"] = date_parse(date).strftime("%Y-%m-%d")
            else:
                context_dict["end_date"] = date_parse(date).strftime("%Y-%m-%d")
        elif re.match(r"[0-9]+-year-old", word):
            context_dict["age"] = int(word.split("-")[0])
        elif word == "years":
            context_dict["age"] = int(filtered_words[i-1])
    return context_dict

with open("examples.txt", "r") as f:
    contexts = f.readlines()
    for ctx in contexts:
        msg = eval(ctx)["message"]
        print(extract_preferences(msg))
        temp_dict = extract_preferences(msg)
        # analysis(temp_dict.get("start_date"), temp_dict.get("end_date"), avoid = [])
    
analysis(start_date="", end_date="", avoid="")