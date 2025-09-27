import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
)

DATA_PATH = os.path.join("data", "processed_comments.csv")
MODEL_PATH = os.path.join("models", "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join("models", "tfidf_vectorizer.pkl")

#Data loading func.
def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Processed data not found at {DATA_PATH}. Run preprocess.py first.")
    
    df = pd.read_csv(DATA_PATH)
    if "preprocessed_text" not in df.columns or "rule_label" not in df.columns:
        raise ValueError("Processed file must contain 'preprocessed_text' and 'rule_label' columns.")
    
    return df

#Training model func.
def train_model():
    print("Loading processed data...")
    df = load_data()
    X = df["preprocessed_text"].astype(str)
    y = df["rule_label"]

    print(f"Loaded {len(df)} samples.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        max_features=5000, #To reduce complexity and save time
        ngram_range=(1, 2) #decides to pick single or pairs
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=300, #maximum number of attempts for the model to learn properly.
        class_weight="balanced",
        random_state=42
    )
    model.fit(X_train_tfidf, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test_tfidf)

    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="weighted", zero_division=0
    )

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, zero_division=0))

    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Vectorizer saved to {VECTORIZER_PATH}")


if __name__ == "__main__":
    train_model()
