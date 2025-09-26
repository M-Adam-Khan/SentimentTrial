#!/usr/bin/env python3
"""
post_discord.py
---------------
Fetches top 5 positive and top 5 negative comments from the SQLite DB
and posts them to a Discord channel via webhook.

Author: Muhammad Adam Khan
"""

import os
import sqlite3
import requests
import pandas as pd

WEBHOOK_URL = "https://discord.com/api/webhooks/1421217656572346450/dzyqg6alAhHEbuan2TLVJ_AVvyWMua2wxA-CcS0bxj4-k1uCRpm-s8cRS8EiG5riz34h"

DB_PATH = os.path.join("data", "comments.db")

def fetch_top_comments(limit=5):
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run save_db.py first.")
    
    conn = sqlite3.connect(DB_PATH)

    pos_df = pd.read_sql_query(
        f"SELECT username, text, score, created_at FROM comments "
        f"WHERE sentiment='positive' ORDER BY score DESC LIMIT {limit}",
        conn
    )

    neg_df = pd.read_sql_query(
        f"SELECT username, text, score, created_at FROM comments "
        f"WHERE sentiment='negative' ORDER BY score DESC LIMIT {limit}",
        conn
    )

    conn.close()
    return pos_df, neg_df

def format_message(df, sentiment_label):
    """
    Formats the DataFrame of comments into a single string message
    suitable for Discord.
    """
    message = f"**Top {len(df)} {sentiment_label} comments:**\n"
    for idx, row in df.iterrows():
        username = row['username']
        text = row['text']
        score = row['score']
        timestamp = row['created_at']
        message += f"\n**{username}** (Score: {score}, {timestamp}):\n{text}\n"
    return message

MAX_DISCORD_LENGTH = 1900  # leave some buffer for formatting

def post_to_discord(message):
    """
    Sends a message to Discord via webhook.
    Splits long messages into chunks under 2000 characters.
    """
    chunks = []
    while len(message) > MAX_DISCORD_LENGTH:
        # split at the last newline before limit
        split_idx = message.rfind("\n", 0, MAX_DISCORD_LENGTH)
        if split_idx == -1:
            split_idx = MAX_DISCORD_LENGTH
        chunks.append(message[:split_idx])
        message = message[split_idx:].lstrip()
    chunks.append(message)

    for chunk in chunks:
        data = {"content": chunk}
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print("Failed to send message:", response.status_code, response.text)


def main():
    print("Fetching top comments from database...")
    pos_df, neg_df = fetch_top_comments(limit=5)

    if not pos_df.empty:
        msg = format_message(pos_df, "Positive")
        post_to_discord(msg)

    if not neg_df.empty:
        msg = format_message(neg_df, "Negative")
        post_to_discord(msg)

if __name__ == "__main__":
    main()
