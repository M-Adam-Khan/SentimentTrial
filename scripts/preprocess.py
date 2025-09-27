#!/usr/bin/env python3
"""
preprocess.py

Step 2 of the SentimentTrial pipeline.

- Reads raw Reddit comments from data/raw_comments.csv
- Cleans & normalizes text (remove links, markdown, bot text, html, etc.)
- Generates sentiment labels using VADER
- Saves processed output to data/processed_comments.csv

"""

import os
import re
import html
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download("punkt")
nltk.download("punkt_tab")   
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("stopwords")
nltk.download("vader_lexicon")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
sia = SentimentIntensityAnalyzer()


#Defining the cleaning Patterns.
URL_PATTERN = re.compile(r"http\S+|www\.\S+")
MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\((http[s]?:\/\/[^\)]+)\)')
MARKDOWN_IMAGE_PATTERN = re.compile(r'!\[.*?\]\(.*?\)')
BOT_PATTERN = re.compile(r"i am a bot", re.IGNORECASE)
HTML_TAG_RE = re.compile(r'<[^>]+>')
USER_SUB_RE = re.compile(r"(u\/\w+|r\/\w+)")


def clean_text(text: str, remove_stopwords=True) -> str:
    if pd.isna(text):
        return ""

    text = html.unescape(str(text)) #convert html entities to normal text.

    text = MARKDOWN_LINK_PATTERN.sub(r"\1", text) #remove markdown links
    text = MARKDOWN_IMAGE_PATTERN.sub("", text) #remove markdown image references

    text = URL_PATTERN.sub("", text) #remove urls

    text = USER_SUB_RE.sub("", text) #remove further references e.g r/subreddit.

    text = HTML_TAG_RE.sub("", text) #remove HTML tags

    if BOT_PATTERN.search(text): #check bot comments
        text = re.sub(BOT_PATTERN, "", text)

    text = re.sub(r"\s+", " ", text).strip() #Normalize Witespaces

    text = text.lower()

    tokens = nltk.word_tokenize(text)
    cleaned_tokens = []
    for tok in tokens:
        if re.fullmatch(r"[\.\,\!\?\:\;'\"]+", tok):
            cleaned_tokens.append(tok)
            continue

        tok_alpha = re.sub(r"[^a-z0-9]", "", tok)
        if not tok_alpha:
            continue

        if remove_stopwords and tok_alpha in stop_words:
            continue

        lemma = lemmatizer.lemmatize(tok_alpha)
        cleaned_tokens.append(lemma)

    return " ".join(cleaned_tokens)


def vader_label(text: str) -> str: #basic type-hinting (input,output = string)
    if not text or str(text).strip() == "":
        return "neutral"
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def preprocess(input_csv="data/raw_comments.csv",
               output_csv="data/processed_comments.csv",
               remove_stopwords=True):
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"{input_csv} not found. Run scrape_reddit.py first.")

    df = pd.read_csv(input_csv)
    print(f"Loaded {len(df)} comments from {input_csv}")

    df["text"] = df["text"].fillna("")

    print("Cleaning text...")
    df["preprocessed_text"] = df["text"].apply(lambda t: clean_text(t, remove_stopwords))

    print("Running VADER sentiment analysis...")
    df["rule_label"] = df["text"].apply(vader_label)

#Handling empty / dropped rows
    before = len(df)
    df = df[df["preprocessed_text"].str.strip() != ""]
    after = len(df)
    if after < before:
        print(f"Dropped {before - after} rows with empty text after cleaning.")

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Saved processed comments to {output_csv}")

    print("\nSentiment distribution:")
    print(df["rule_label"].value_counts())

    return df

if __name__ == "__main__":
    preprocess()
