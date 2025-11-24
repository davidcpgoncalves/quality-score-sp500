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

# Get financial data from yfinance
import yfinance as yf

def get_fundamental_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return{
        "ticker": ticker,
        "market-cap": info.get("marketCap", "N/A"),
        "ebitda": info.get("ebitda", "N/A"),
        "pe-ratio": info.get("trailingPE", "N/A"),
        "pb-ratio": info.get("priceToBook", "N/A"),
        "ps-ratio": info.get("priceToSalesTrailing12Months", "N/A"),
        "dividend-yield": info.get("dividendYield", "N/A"),
        "current-price": info.get("currentPrice", "N/A"),
    }

tickers = df["Symbol"].head(20)
fundamental_data = [get_fundamental_data(ticker) for ticker in tickers]
fundamentals_df = pd.DataFrame(fundamental_data)