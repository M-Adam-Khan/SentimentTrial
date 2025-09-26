import os
import sqlite3
import pandas as pd

CSV_PATH = os.path.join("data", "processed_comments.csv")
DB_PATH = os.path.join("data", "comments.db")

def save_to_db():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Processed data not found at {CSV_PATH}. Run preprocess.py first.")

    print("Loading processed CSV...")
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT,
            comment_id TEXT,
            parent_id TEXT,
            username TEXT,
            text TEXT,
            preprocessed_text TEXT,
            sentiment TEXT,
            score INTEGER,
            created_at TEXT
        );
    """)

    print("Inserting data into database...")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO comments (
                post_id, comment_id, parent_id, username, text, preprocessed_text,
                sentiment, score, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("post_id"),
            row.get("comment_id"),
            row.get("parent_id"),
            row.get("username"),
            row.get("text"),
            row.get("preprocessed_text"),
            row.get("rule_label"),  
            row.get("score"),
            row.get("created_at")
        ))

    conn.commit()
    conn.close()
    print(f"Data successfully saved to {DB_PATH}")

if __name__ == "__main__":
    save_to_db()
