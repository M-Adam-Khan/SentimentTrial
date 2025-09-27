SentimentTrial

SentimentTrial is a Python project that scrapes Reddit comments, analyzes their sentiment using NLP and machine learning, stores results in a database, and can automatically post top comments to Discord. It demonstrates a full AI/ML workflow, from data collection to reporting and automation.

Project Overview

This project enables users to:

Collect user-generated content from Reddit posts.

Perform sentiment analysis (Positive, Negative, Neutral) using NLP.

Train a machine learning classifier to predict sentiment from text.

Store processed comments and predictions in a SQLite database.

Automatically share top positive and negative comments via Discord webhook.

The solution demonstrates a real-world AI workflow with logging, error handling, and automation.

Requirements

Python 3.10+

Virtual environment (venv)

Reddit API credentials (script-based app)

Discord webhook URL (optional, for posting top comments)

Installed Python packages via requirements.txt

Setup & Installation

Get the credentials from reddit and Discord
put them into the .env file:
CLIENT_ID=your_reddit_client_id_here
CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USERNAME=your_reddit_username_here
PASSWORD=your_reddit_password_here
USER_AGENT=your_user_agent_here
DISCORD_WEBHOOK_URL=your_discord_webhook_here

Create and activate a virtual environment

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Usage

Run the full pipeline with:

python scripts/run_all.py

This script will:

Scrape comments from a Reddit post.

Preprocess comments and analyze sentiment using VADER.

Train a Logistic Regression model on TF-IDF features.

Save processed comments and predictions in a SQLite database.

Display top 5 positive and negative comments in the console.

Post top comments to your configured Discord webhook (if provided).

Output

CSV Files:

data/raw_comments.csv – raw scraped comments

data/processed_comments.csv – processed comments with sentiment analysis

Database:

data/comments.db – SQLite database containing all comments and predictions

Models:

models/sentiment_model.pkl – trained ML model

models/tfidf_vectorizer.pkl – trained TF-IDF vectorizer

Discord Notifications:
Top positive and negative comments automatically posted.

Logging & Progress

While scraping, the script will print logs for:

Total comments found and collected

Number of comments processed (every 20 comments)

Any errors or skipped comments

This ensures visibility into long-running scraping tasks.

Notes

The SQLite database will be overwritten each time run_all.py is executed.

Only top-level comments are collected to speed up scraping.

Discord posting requires a valid webhook. If omitted, only local storage will occur.

Python 3.10+ is recommended for compatibility.

LOOM VIDEO LINK:
https://www.loom.com/share/dcaf09adeaab47c0aa9891f70348ef07?sid=6e15e4e5-8a30-45e8-85fd-045242e048ef