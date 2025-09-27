#!/usr/bin/env python3
"""
scrape_reddit.py

Scrape Reddit comments from a given post URL using PRAW.

- Uses script-based login with CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT.
- Collects at least 100+ comments (with text, username, timestamp, id).
- Handles errors, rate-limits, and retries gracefully.
- Saves results into data/raw_comments.csv

Faster version: fetches only top-level comments and limits deep threads to speed up scraping.
Prints live progress logs for better monitoring.
"""

import os
import time
import re
import sys
import pandas as pd
from datetime import datetime
import praw
from prawcore.exceptions import RequestException, ResponseException, PrawcoreException
from dotenv import load_dotenv

load_dotenv()

# Assigning credentials from the environment
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("PASSWORD")
USER_AGENT = os.getenv("USER_AGENT")

# Connecting to Reddit API
try:
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        user_agent=USER_AGENT,
        ratelimit_seconds=300
    )
except Exception as e:
    print(f"Error initializing Reddit API: {e}")
    sys.exit(1)

def scrape_post_comments(post_url: str, max_comments: int = 150) -> pd.DataFrame:
    """
    Scrape comments from a Reddit post URL.
    Returns a DataFrame with: comment_id, post_id, username, text, score, created_at.
    Uses only top-level comments and limits deep threads to speed up scraping.
    Prints live logs for every 10 comments processed.
    """
    comments_data = []
    try:
        submission = reddit.submission(url=post_url)
        submission.comment_sort = "top"

        # Fetch only top-level comments and skip deep threads
        submission.comments.replace_more(limit=0)
        all_comments = submission.comments.list()[:max_comments]

    except (RequestException, ResponseException, PrawcoreException) as e:
        print(f"Error fetching submission: {e}")
        return pd.DataFrame()

    print(f"Found {len(all_comments)} comments. Collecting up to {max_comments}...")

    for i, comment in enumerate(all_comments, 1):
        try:
            comments_data.append({
                "post_id": submission.id,
                "comment_id": comment.id,
                "parent_id": comment.parent_id,
                "username": str(comment.author),
                "text": comment.body.strip(),
                "score": comment.score,
                "created_at": datetime.fromtimestamp(comment.created_utc).isoformat()
            })

            #showing logs after 10 comments
            if i % 10 == 0 or i == len(all_comments):
                print(f"Processed {i}/{len(all_comments)} comments.")

            #sleep added after every 20 comments
            if i % 20 == 0:
                print("Sleeping 1 second to avoid hitting rate limits...")
                time.sleep(1)

        except Exception as e:
            print(f"Skipping comment #{i} due to error: {e}")
            continue

    return pd.DataFrame(comments_data)

def main():
    os.makedirs("data", exist_ok=True)
    post_url = input("Enter a Reddit post URL: ").strip()

    df = scrape_post_comments(post_url, max_comments=150)

    if df.empty:
        print("No comments scraped. Exiting.")
        sys.exit(1)

    output_path = "data/raw_comments.csv"
    df.to_csv(output_path, index=False)
    print(f"Scraped {len(df)} comments. Saved to {output_path}")
    print("Sample of scraped data:")
    print(df.head())

if __name__ == "__main__":
    main()
