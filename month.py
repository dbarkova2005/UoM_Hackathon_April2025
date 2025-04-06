import yfinance as yf

tickers = ["JPM", "BAC", "WFC", "PGR", "GS", "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "ISRG", "AMGN", "GILD", "VRTX", "REGN", "ALNY", "AMT", "PLD", "PSA", "DLR", "UPS", "UNP", "CSX", "LUV", "PAA", "MMM", "CAT", "DE", "AMAT", "GE", "HON"]
month_codes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
main_dict = {}

for ticker in tickers:
    year = "2005"
    temp_dict = {}
    while int(year) <= 2025:
        for i in range(12):
            start_year = year+"-"+month_codes[i]+"-01"
            if int(year) <= 2025:
                end_year = year+"-"+month_codes[(i+1)%12]+"-01"
                data = yf.download(ticker, start=start_year, end=end_year)
            open_price = data['Close'][ticker].iloc[0]
            mean = data[('Close', ticker)].mean()
            temp_dict[int(year)] = float(mean)
            year = str(int(year) + 1)

    main_dict[ticker] = temp_dict

print(main_dict)

with open("mean.txt", "w") as f:
    f.write(str(main_dict))