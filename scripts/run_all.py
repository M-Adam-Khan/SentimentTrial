"""
run_all.py
==========

Orchestrates the full SentimentTrial pipeline end-to-end.

Workflow:
1. Scrapes Reddit comments from a given post URL.
2. Preprocesses and cleans the scraped comments.
3. Trains a sentiment analysis model using Logistic Regression and TF-IDF features.
4. Saves the processed comments to an SQLite database.
5. Queries the database to display top positive/negative comments and sentiment distribution.
6. Posts the top comments to a Discord channel via webhook.

Each step is executed sequentially using the corresponding script in the 'scripts/' folder.

"""

import os
import subprocess
import sqlite3
import pandas as pd

DB_PATH = os.path.join("data", "comments.db")

REDDIT_POST_URL = "https://www.reddit.com/r/politics/comments/1nr5x4r/oversight_democrats_release_third_batch_of/"

def run_step(script_name, input_text=None):
    print(f"\n=== Running {script_name} ===")
    try:
        result = subprocess.run(
            ["python", os.path.join("scripts", script_name)],
            input=input_text,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:\n", result.stderr)
    except Exception as e:
        print(f"Error running {script_name}: {e}")

def query_db():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Run save_db.py first.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    print("\n=== Top 5 Positive Comments ===")
    pos_df = pd.read_sql_query(
        "SELECT username, text, sentiment, score, created_at "
        "FROM comments WHERE sentiment='positive' "
        "ORDER BY score DESC LIMIT 5",
        conn
    )
    print(pos_df.to_string(index=False))

    print("\n=== Top 5 Negative Comments ===")
    neg_df = pd.read_sql_query(
        "SELECT username, text, sentiment, score, created_at "
        "FROM comments WHERE sentiment='negative' "
        "ORDER BY score DESC LIMIT 5",
        conn
    )
    print(neg_df.to_string(index=False))

    print("\n=== Sentiment Distribution ===")
    dist_df = pd.read_sql_query(
        "SELECT sentiment, COUNT(*) as count FROM comments GROUP BY sentiment",
        conn
    )
    print(dist_df.to_string(index=False))

    conn.close()

def main():
    run_step("scrape_reddit.py", input_text=REDDIT_POST_URL + "\n")
    run_step("preprocess.py")
    run_step("train_model.py")
    run_step("save_db.py")
    
    query_db()
    
    run_step("post_discord.py")

if __name__ == "__main__":
    main()
