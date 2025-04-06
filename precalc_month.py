import yfinance as yf
import pandas as pd

tickers = ["JPM", "BAC", "WFC", "PGR", "GS", "AAPL", "MSFT", "NVDA", "GOOG", "AMZN",
           "ISRG", "AMGN", "GILD", "VRTX", "REGN", "ALNY", "AMT", "PLD", "PSA", "DLR",
           "UPS", "UNP", "CSX", "LUV", "PAA", "MMM", "CAT", "DE", "AMAT", "GE", "HON"]

main_dict = {}

for ticker in tickers:
    temp_dict = {}
    for year in range(2005, 2026):  # 2005 to 2025 inclusive
        for month in range(1, 13):  # January to December
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year+1}-01-01"
            else:
                end_date = f"{year}-{month+1:02d}-01"

            try:
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not data.empty:
                    mean_close = data['Close'].mean()
                    temp_dict[f"{year}-{month:02d}"] = float(mean_close.item())
            except Exception as e:
                pass  # skip this month if data download fails

    main_dict[ticker] = temp_dict

print(main_dict)

# # Optional: convert to a DataFrame if you want tabular format
# df = pd.DataFrame(main_dict)
# print(df)
