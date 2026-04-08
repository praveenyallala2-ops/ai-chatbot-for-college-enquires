"""
nlp_engine.py
─────────────────────────────────────────────────────────────────────────────
Handles all NLP pre-processing and intent classification.

Pipeline:
  1. Tokenisation        – split text into word tokens
  2. Stop-word removal   – filter common English stop words
  3. TF-IDF vectorisation – convert cleaned tokens to feature vector
  4. Naive Bayes classifier (via scikit-learn) – classify intent
"""

import re
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# ──────────────────────────────────────────────────────────────────────────────
# STOP WORDS  (common English words that carry little information)
# We keep a focused list so the vectoriser concentrates on meaningful words
# ──────────────────────────────────────────────────────────────────────────────
STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if", "or", "because", "as",
    "until", "while", "of", "at", "by", "for", "with", "about",
    "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on",
    "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "both",
    "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "s", "t", "can", "will", "just", "don", "should", "now",
    "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "couldn",
    "didn", "doesn", "hadn", "hasn", "haven", "isn", "ma", "mightn",
    "mustn", "needn", "shan", "shouldn", "wasn", "weren", "won", "wouldn"
}

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'chatbot_model.pkl')


# ──────────────────────────────────────────────────────────────────────────────
# STEP 1 – TOKENISATION
# ──────────────────────────────────────────────────────────────────────────────
def tokenize(text: str) -> list[str]:
    """
    Lowercase and split text into word tokens.
    Removes punctuation and non-alphabetic characters.
    """
    text = text.lower()
    tokens = re.findall(r'[a-z]+', text)   # keep only alphabetic words
    return tokens


# ──────────────────────────────────────────────────────────────────────────────
# STEP 2 – STOP-WORD REMOVAL
# ──────────────────────────────────────────────────────────────────────────────
def remove_stopwords(tokens: list[str]) -> list[str]:
    """
    Filter out stop words from the token list.
    Preserves domain-specific terms even if short (e.g. 'fee', 'cse').
    """
    return [t for t in tokens if t not in STOP_WORDS or len(t) <= 3]


# ──────────────────────────────────────────────────────────────────────────────
# COMBINED PRE-PROCESSOR  (used by TfidfVectorizer's analyzer)
# ──────────────────────────────────────────────────────────────────────────────
def preprocess(text: str) -> str:
    """
    Tokenise → remove stop words → rejoin as string.
    TfidfVectorizer expects a string (it will re-tokenise internally via
    its own word-boundary splitter, but we have cleaned the content first).
    """
    tokens = tokenize(text)
    cleaned = remove_stopwords(tokens)
    return " ".join(cleaned) if cleaned else text.lower()


# ──────────────────────────────────────────────────────────────────────────────
# STEP 3 + 4 – TF-IDF VECTORISATION  +  NAIVE BAYES CLASSIFIER
# Wrapped together in a scikit-learn Pipeline for clean predict()
# ──────────────────────────────────────────────────────────────────────────────
def build_pipeline() -> Pipeline:
    """
    Returns an untrained sklearn Pipeline:
      TfidfVectorizer  →  MultinomialNB
    """
    return Pipeline([
        (
            'tfidf',
            TfidfVectorizer(
                analyzer='word',
                ngram_range=(1, 2),      # unigrams + bigrams
                min_df=1,
                sublinear_tf=True        # apply log(1+tf) smoothing
            )
        ),
        (
            'clf',
            MultinomialNB(alpha=0.3)     # Laplace smoothing factor
        )
    ])


def train(phrases: list[str], labels: list[str]) -> Pipeline:
    """
    Pre-process all phrases, then fit the TF-IDF + NB pipeline.
    Returns the trained Pipeline object.
    """
    cleaned = [preprocess(p) for p in phrases]
    pipeline = build_pipeline()
    pipeline.fit(cleaned, labels)
    return pipeline


def save_model(pipeline: Pipeline) -> None:
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"[NLP] Model saved → {MODEL_PATH}")


def load_model() -> Pipeline:
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def predict_intent(pipeline: Pipeline, user_input: str) -> tuple[str, float]:
    """
    Classify user_input and return (intent_name, confidence_score).
    confidence_score is the highest class probability from NB.
    """
    cleaned = preprocess(user_input)
    intent = pipeline.predict([cleaned])[0]
    proba  = pipeline.predict_proba([cleaned])[0]
    confidence = float(max(proba))
    return intent, confidence
