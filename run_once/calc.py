import yfinance as yf

tickers = ["JPM", "BAC", "WFC", "PGR", "GS", "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "ISRG", "AMGN", "GILD", "VRTX", "REGN", "ALNY", "AMT", "PLD", "PSA", "DLR", "UPS", "UNP", "CSX", "LUV", "PAA", "MMM", "CAT", "DE", "AMAT", "GE", "HON"]

main_dict = {}

for ticker in tickers:
    year = "2005"
    temp_dict = {}
    while int(year) <= 2025:
        start_year = year+"-01-01"
        if int(year) < 2025:
            end_year = str(int(year)+1)+"-01-01"
            data = yf.download(ticker, start=start_year, end=end_year)
        else:
            data = yf.download(ticker, start=start_year)

        open_price = data['Close'][ticker].iloc[0]
        std = data[('Close', ticker)].std()
        mean = data[('Close', ticker)].mean()
        result = std/mean
        temp_dict[int(year)] = float(result)

        year = str(int(year) + 1)

    main_dict[ticker] = temp_dict

print(main_dict)

with open("risk.txt", "w") as f:
    f.write(str(main_dict))