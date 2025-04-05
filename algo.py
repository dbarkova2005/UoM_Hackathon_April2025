import yfinance as yf
dat = yf.Ticker("MSFT")
print(dat.info["sector"])
print(dat.info["industry"])
print(dat.history(period='1y'))

# var
# age & risk


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