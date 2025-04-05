import yfinance as yf
dat = yf.Ticker("MSFT")
print(dat.info["sector"])
print(dat.info["industry"])
print(dat.history(period='1y'))

# var
# age & risk


def extract_preferences(message: str):
    print("TODO")
    print(message)
    return