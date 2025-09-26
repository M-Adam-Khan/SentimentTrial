SentimentTrial

SentimentTrial is a Python project that scrapes Reddit comments, analyzes their sentiment using NLP and machine learning, stores results in a database, and can post top comments to Discord. It demonstrates a full AI/ML workflow from data collection to deployment.

Reddit API Note: To run this project, you need to create a Reddit app for script-based access. Go to Reddit Apps
, click Create App, choose script, and note your CLIENT_ID and CLIENT_SECRET.

Requirements

Python 3.10+

Virtual environment (venv)

Reddit API credentials

Discord webhook URL

Setup & Installation

Clone the repository:

git clone https://github.com/M-Adam-Khan/SentimentTrial.git
cd SentimentTrial


Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Create a .env file in the root directory with your Reddit credentials:

CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
PASSWORD=your_reddit_password
USER_AGENT=your_user_agent

Usage

Run the full pipeline with:

python scripts/run_all.py


This will:

Scrape comments from a Reddit post.

Preprocess comments and analyze sentiment using VADER.

Train a Logistic Regression model on TF-IDF features.

Save processed comments and predictions in a SQLite database.

Display top 5 positive and negative comments.

Post these top comments to your configured Discord webhook.

Output

CSV files: data/raw_comments.csv and data/processed_comments.csv

Database: data/comments.db

Models: models/sentiment_model.pkl and models/tfidf_vectorizer.pkl

Discord notifications: Top positive and negative comments automatically posted