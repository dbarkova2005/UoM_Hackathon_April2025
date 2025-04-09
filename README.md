# QuantCat StudentHack2025

We were tasked to create an algorithm which designed investment portfolios with the exact number of shares for each ticker based on client needs. For each request, we were given details about the client's age, investment period, salary, budget and disliked sectors. All of this needed to be returned in just **two seconds** (10 seconds in earlier rounds).

## The Algorithm

### 0. Downloading Prices & Estimating Risk

We used yfinance to download the stock prices for each of our selected stocks and kept a cache of the prices over the last 20 years. We also estimated the risk for each stock with the standard deviation in the stock price divided by the mean in the stock price for each year. We knew that network bandwidth is the limiting factor when it comes to high frequency, so downloading all the data once and caching allowed us to excel in the high frequency rounds. We stored the price and "risk" data in text files as 2D Python dictionaries like so:

```python
{"AAPL": {2005: 10, 2006: 12, 2007: 14, ...}, "MSFT": {2005: 14, 2006: 15, 2007: 18, ...}, ...}
```

### 1. Data Extraction

First, we took the sentences provided for each client and extracted the information. Each request had a few sentences similar to this one:

```python
   
"Kristin Davis is a 44-year-old female investor who started investing on March 28th, 2008 and ended on February 26th, 2009. She enjoys rock climbing and avoids manufacturing, structured finance, trade and services, and life sciences. She has a budget of $1075 per year."

```

We then used this to create a Python dictionary using the Natural Language Toolkit and regular expressions to get something like this:

```python
{"start": "2008-03-28", "end": "2009-02-26", "age": 44,
  "budget": 985, 'dislikes': ['finance', 'life science', 'manufacturing'],
  "salary": None
}
```

It is worth noting that since our method to extract this data worked on structural assumptions of the sentences provided, the parsing often failed, and we would just skip the input. This was necessary since the sentences were generated by a low-parameter LLM, which tended to hallucinate.

This dictionary was actually given to us in rounds 4 and 5 (which we won)

### 2. Filtering Sectors

We stored a dictionary of about 30 trusted stocks, grouped by the sectors that came up from the server. We arbitrarily picked these since they were good performers between 2000 and 2025 which all of the dates of the requests fell.

```python
symbols = {
    "finance": ["JPM", "BAC", "WFC", "PGR", "GS"],
    "technology": ["AAPL", "MSFT", "NVDA", "GOOG", "AMZN"],
    "life science": ["ISRG", "AMGN", "GILD", "VRTX", "REGN", "ALNY"],
    "real estate": ["AMT", "PLD", "PSA", "DLR"],
    "energy": ["PAA", "UPS", "UNP", "CSX", "LUV"],
    "manufacturing": ["MMM", "CAT", "DE", "AMAT", "GE", "HON"],
}
```

Choosing this particular list was extremely helpful since they were publicly traded between 2000 and 2025. This means we did not need to worry about filtering stocks out based on time, which would lead to a point penalty for failing to do so.

Once we recognised the disliked sectors, we would pass a list of all tickers through to the next step. Following on from our example, the algorithm will go forth with this list of tickers:

```python
["AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "AMT", "PLD", "PSA", "DLR", "PAA", "UPS", "UNP", "CSX", "LUV"]
```

In this step, we also only picked stocks that led to a more than 60% ROI over the given time frame based on historical data, maximising our profit. We tweaked this value from just 10% to 60% as the challenge progressed. For this example, I will ignore this filter.


### 3. Calculating Risk Tolerance

We had to curate our portfolios conscious to the risk tolerance of clients. We used a simple 3-class system to do so. Here is the function:

```python

# ratio is total budget over salary
# If no salary was given (e.g. unemployed client), we give them low risk

def calculate_risk(age: int, employed: bool, ratio: float):
    if ratio > 0.3:
        return "low"
    if ratio < 0.05:
        return "high"
    if not employed:
        return "low"
    elif age == -1:   # age of -1 is for when we failed to extract the age (usually due to LLM hallucinations)
        return "medium"
    elif age < 30:
        return "high"
    elif 30 <= age <= 60:
        return "medium" 
    return "low"
```

In our example, Kristin has a low risk tolerance.

### 4. Tuning Tickers for Risk

We now take our list of stocks from step two and remove the ones considered too risky or too safe based on the client's risk tolerance.

If the client's risk was "medium", we would do nothing. If it was "low", we would remove the top 30% riskiest stocks, and if their tolerance was "high", we would remove the 30% of the stocks deemed the least risky. The "risk" was precomputed in step 0.

Since Kristin is wants low risk, we are now going to use this list for our portfolio:

```python
['MSFT', 'GOOG', 'AMT', 'PSA', 'DLR', 'PAA', 'UPS', 'UNP', 'LUV']
```

### 5. Choosing Quantities

To do this, we just had to pick any distribution that didn't breach the budget. We didn't overthink it and just went for a portfolio balanced in the number of shares. We would sort our list in order of descending start price and then add one share into the portfolio if it still fit the budget.

With our example, we would return this to the server:

```python
  {'PSA': 2, 'UPS': 2, 'AMT': 2, 'UNP': 2, 'MSFT': 1, 'DLR': 1, 'GOOG': 1, 'LUV': 1, 'PAA': 2}
```
