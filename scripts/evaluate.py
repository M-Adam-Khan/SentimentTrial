import os
import joblib

MODEL_PATH = os.path.join("models", "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join("models", "tfidf_vectorizer.pkl")

def load_model_and_vectorizer():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Trained model or vectorizer not found. Run train_model.py first.")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def evaluate(new_texts):
    model, vectorizer = load_model_and_vectorizer()
    X_new = vectorizer.transform(new_texts)
    y_pred = model.predict(X_new)
    print("\n=== Predictions ===")
    for text, pred in zip(new_texts, y_pred):
        print(f"Text: {text}\nPredicted Sentiment: {pred}\n")

    return y_pred

if __name__ == "__main__":
    test_texts = [
        "Great Product! Loved it",
        "The product was okay, nothing special.",
        "Worst experience ever. Totally disappointed."
    ]

    test_labels = ["positive", "neutral", "negative"]

    evaluate(test_texts)
