import sqlite3
import pandas as pd
import numpy as np

def execute_sql_pipeline():
    """Executes structural cleansing in SQL and calculates dynamic rolling baselines in Pandas."""
    conn = sqlite3.connect("data/market_compliance.db")
    
    # 1. Cleanse raw strings, handle zero values, and sort chronologically
    sql_query = """
    SELECT 
        Date,
        COALESCE(NULLIF(Volume, 0), 100000) AS Volume,
        Close
    FROM raw_market_ledger
    ORDER BY Date ASC;
    """
    
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    
    if df.empty:
        raise ValueError("❌ Staged database table is empty. Run data_ingestion.py first.")

    print("🧼 SQL data extraction complete. Calculating rolling baselines...")

    # 2. Replicate the complex window function logic using Pandas rolling operations
    # shifts by 1 to exclude the current record row from its own historical baseline
    df['rolling_mean_volume'] = df['Volume'].shift(1).rolling(window=90, min_periods=1).mean()
    df['rolling_std_volume'] = df['Volume'].shift(1).rolling(window=90, min_periods=1).std()

    # 3. Handle cold-start rows (the first few rows that don't have historical variance yet)
    df['rolling_mean_volume'] = df['rolling_mean_volume'].fillna(df['Volume'])
    df['rolling_std_volume'] = df['rolling_std_volume'].fillna(1.0)
    df['rolling_std_volume'] = df['rolling_std_volume'].replace(0.0, 1.0) # Prevent division by zero

    # Save to local data folder for modeling ingestion
    df.to_csv("data/engineered_features.csv", index=False)
    print("✅ Feature engineering complete. Saved to 'data/engineered_features.csv'.")
    return df

if __name__ == "__main__":
    execute_sql_pipeline()