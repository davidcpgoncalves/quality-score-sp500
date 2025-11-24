# Importing libs to get data
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Using the wikipedia's API with User-agent mode
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
headers = {
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Continuing processing data with beautiful soup (getting data into a pandas dataframe)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", {"id": "constituents"})
df = pd.read_html(str(table))[0]

# Get financial data from yahooquery
from yahooquery import Ticker

tickers = list(df["Symbol"].head(10))
yq_tickers = Ticker(tickers)
info = yq_tickers.summary_detail

fundamental_data = []

for ticker in tickers:
    # Get multiple modules for each ticker, fallback to {} if missing
    summary_detail = yq_tickers.summary_detail.get(ticker, {})
    key_stats = yq_tickers.key_stats.get(ticker, {})
    financial_data = yq_tickers.financial_data.get(ticker, {})
    
    record = {
        "ticker": ticker,
        "marketCap": summary_detail.get("marketCap", "N/A"),
        "ebitda": key_stats.get("ebitda", financial_data.get("ebitda", "N/A")),
        "peRatio": summary_detail.get("trailingPE", "N/A"),
        "pbRatio": summary_detail.get("priceToBook") or financial_data.get("priceToBook") or "N/A",
        "psRatio": summary_detail.get("priceToSalesTrailing12Months","N/A"),
        "dividendYield": summary_detail.get("dividendYield"),
        "currentPrice": financial_data.get("currentPrice", "N/A"),
    }
    fundamental_data.append(record)

fundamentals_df = pd.DataFrame(fundamental_data)