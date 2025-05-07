import gzip
import json
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle

# Globals
titles = None
tfidf = None
vectorizer = None
books_titles = None
csv_book_mapping = None
interactions_df = None

def parse_fields(line):
    data = json.loads(line)
    return {
        "book_id": data["book_id"], 
        "title": data["title_without_series"], 
        "ratings": data["ratings_count"], 
        "url": data["url"], 
        "cover_image": data["image_url"]
    }

def load_and_prepare(book_path, id_map_path, interactions_path):
    global titles, tfidf, vectorizer, books_titles, csv_book_mapping, interactions_df

    if os.path.exists("cache.pkl"):
        print("Loading cached data...")
        with open("cache.pkl", "rb") as f:
            titles, tfidf, vectorizer, books_titles, csv_book_mapping, interactions_df = pickle.load(f)
        return

    print("1. Processing book metadata...")
    books_data = []
    with gzip.open(book_path) as f:
        for line in f:
            try:
                fields = parse_fields(line)
                if int(fields["ratings"]) > 5:
                    books_data.append(fields)
            except Exception:
                continue

    titles = pd.DataFrame.from_dict(books_data)
    titles["ratings"] = pd.to_numeric(titles["ratings"], errors="coerce")
    titles["mod_title"] = titles["title"].str.replace("[^a-zA-Z0-9 ]", "", regex=True).str.lower()
    titles["mod_title"] = titles["mod_title"].str.replace(r"\s+", " ", regex=True)
    titles = titles[titles["mod_title"].str.len() > 0].reset_index(drop=True)

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(titles["mod_title"])
    books_titles = titles.copy()

    print("2. Loading book ID map...")
    csv_book_mapping = {}
    with open(id_map_path) as f:
        for line in f:
            csv_id, book_id = line.strip().split(",")
            csv_book_mapping[csv_id] = book_id

    print("3. Loading user interaction data...")
    interactions_df = pd.read_csv(interactions_path, names=["user_id", "csv_id", "timestamp", "rating", "extra"], low_memory=False)

    with open("cache.pkl", "wb") as f:
        pickle.dump((titles, tfidf, vectorizer, books_titles, csv_book_mapping, interactions_df), f)
    print("Cached data to 'cache.pkl'")

def search_books(query):
    processed = re.sub("[^a-zA-Z0-9 ]", "", query.lower())
    query_vec = vectorizer.transform([processed])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]
    results = titles.iloc[indices]
    results = results.sort_values("ratings", ascending=False)
    return results.head(5)[["title", "ratings", "url", "cover_image"]].to_dict(orient="records")

def recommend_books(liked_books, top_n=10):
    global interactions_df, csv_book_mapping, books_titles

    liked_set = set(liked_books)
    overlap_users = set()

    for _, row in interactions_df.iterrows():
        book_id = csv_book_mapping.get(str(row["csv_id"]))
        if not book_id:
            continue
        try:
            rating = int(row["rating"])
            if book_id in liked_set and rating >= 4:
                overlap_users.add(row["user_id"])
        except:
            continue

    rec_lines = []
    for _, row in interactions_df.iterrows():
        if row["user_id"] in overlap_users:
            book_id = csv_book_mapping.get(str(row["csv_id"]))
            if book_id:
                rec_lines.append(book_id)

    if not rec_lines:
        return []

    rec_counts = pd.Series(rec_lines).value_counts().reset_index()
    rec_counts.columns = ["book_id", "book_count"]

    rec_df = rec_counts.copy()
    rec_df["book_id"] = rec_df["book_id"].astype(str)
    books_titles["book_id"] = books_titles["book_id"].astype(str)

    rec_df = rec_df.merge(books_titles, on="book_id", how="inner")
    rec_df["ratings"] = pd.to_numeric(rec_df["ratings"], errors="coerce")
    rec_df = rec_df[rec_df["ratings"] > 0]
    rec_df["score"] = rec_df["book_count"] * (rec_df["book_count"] / rec_df["ratings"])
    rec_df = rec_df[~rec_df["book_id"].isin(liked_books)]
    rec_df = rec_df.sort_values("score", ascending=False)

    return rec_df.head(top_n)[["book_id", "title", "score", "url", "cover_image"]].to_dict(orient="records")
