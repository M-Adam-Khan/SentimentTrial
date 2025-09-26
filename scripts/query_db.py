import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("data", "comments.db")

def fetch_comments(query, limit=5):
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run save_db.py first.")

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    print("\n=== Top 5 Positive Comments ===")
    positive_df = fetch_comments(
        "SELECT username, text, sentiment, score, created_at "
        "FROM comments WHERE sentiment='positive' "
        "ORDER BY score DESC LIMIT 5"
    )
    print(positive_df.to_string(index=False))

    print("\n=== Top 5 Negative Comments ===")
    negative_df = fetch_comments(
        "SELECT username, text, sentiment, score, created_at "
        "FROM comments WHERE sentiment='negative' "
        "ORDER BY score DESC LIMIT 5"
    )
    print(negative_df.to_string(index=False))

    print("\n=== Sentiment Distribution ===")
    dist_df = fetch_comments(
        "SELECT sentiment, COUNT(*) as count FROM comments GROUP BY sentiment"
    )
    print(dist_df.to_string(index=False))

if __name__ == "__main__":
    main()
