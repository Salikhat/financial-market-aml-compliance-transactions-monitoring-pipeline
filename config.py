import os

# Configuration Settings
TICKER_SYMBOL = "^GDAXI"  # DAX Index (Deutsche Börse Core Market Benchmark)
START_DATE = "2024-01-01"
LOOKBACK_DAYS = 90
Z_SCORE_THRESHOLD = 3.0

# Ensure data output directories exist
os.makedirs("data", exist_ok=True)