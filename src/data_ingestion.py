import yfinance as yf
import pandas as pd
import sqlite3
import sys
import os

# Append parent directory to path to allow config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def fetch_live_market_data():
    """Fetches real-time historical market data from an open API source."""
    print(f"📡 Querying open API for ticker: {config.TICKER_SYMBOL}...")
    ticker = yf.Ticker(config.TICKER_SYMBOL)
    df = ticker.history(start=config.START_DATE, interval="1d")
    
    if df.empty:
        raise ValueError("❌ Failed to fetch data from API source.")
        
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df[['Date', 'Volume', 'Close']]

def stage_to_relational_db(df):
    """Stages raw extracted data into an in-memory SQLite database to simulate production warehouses."""
    conn = sqlite3.connect("data/market_compliance.db")
    df.to_sql("raw_market_ledger", conn, if_exists="replace", index=False)
    print("💾 Data successfully staged in relational DB table: 'raw_market_ledger'.")
    conn.close()

if __name__ == "__main__":
    market_data = fetch_live_market_data()
    stage_to_relational_db(market_data)