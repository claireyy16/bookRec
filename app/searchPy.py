import gzip
import json
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def parse_fields(line):
    data = json.loads(line)
    return {
        "book_id": data["book_id"], 
        "title": data["title_without_series"], 
        "ratings": data["ratings_count"], 
        "url": data["url"], 
        "cover_image": data["image_url"]
    }

# Global cache
titles = None
tfidf = None
vectorizer = None

def load_and_prepare(path="goodreads_books.json.gz"):
    global titles, tfidf, vectorizer

    books_titles = []
    with gzip.open(path) as f:
        for line in f:
            fields = parse_fields(line)
            try:
                ratings = int(fields["ratings"])
            except ValueError:
                continue
            if ratings > 5:
                books_titles.append(fields)

    titles = pd.DataFrame.from_dict(books_titles)
    titles["ratings"] = pd.to_numeric(titles["ratings"])
    titles["mod_title"] = titles["title"].str.replace("[^a-zA-Z0-9 ]", "", regex=True)
    titles["mod_title"] = titles["mod_title"].str.lower()
    titles["mod_title"] = titles["mod_title"].str.replace("\s+", " ", regex=True)
    titles = titles[titles["mod_title"].str.len() > 0]
    titles.reset_index(drop=True, inplace=True)

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(titles["mod_title"])

def search_books(query):
    processed = re.sub("[^a-zA-Z0-9 ]", "", query.lower())
    query_vec = vectorizer.transform([processed])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:]
    results = titles.iloc[indices]
    results = results.sort_values("ratings", ascending=False)
    return results.head(5)[["title", "ratings", "url", "cover_image"]].to_dict(orient="records")

def recommend_books(liked_books, top_n=10):
    csv_book_mapping = {}
    with open("book_id_map.csv", "r") as f:
        for line in f:
            csv_id, book_id = line.strip().split(",")
            csv_book_mapping[csv_id] = book_id

    overlap_users = set()
    with open("goodreads_interactions.csv", "r") as f:
        for line in f:
            user_id, csv_id, _, rating, _ = line.strip().split(",")
            try:
                rating = int(rating)
            except ValueError:
                continue

            book_id = csv_book_mapping.get(csv_id)
            if book_id in liked_books and rating >= 4:
                overlap_users.add(user_id)

    rec_lines = []
    with open("goodreads_interactions.csv", "r") as f:
        for line in f:
            user_id, csv_id, _, rating, _ = line.strip().split(",")
            if user_id in overlap_users:
                book_id = csv_book_mapping.get(csv_id)
                rec_lines.append([user_id, book_id, rating])

    recs = pd.DataFrame(rec_lines, columns=["user_id", "book_id", "rating"])
    recs["book_id"] = recs["book_id"].astype(str)

    all_recs = recs["book_id"].value_counts().to_frame().reset_index()
    all_recs.columns = ["book_id", "book_count"]

    books_titles = pd.read_json("books_titles.json")
    books_titles["book_id"] = books_titles["book_id"].astype(str)

    all_recs = all_recs.merge(books_titles, how="inner", on="book_id")
    all_recs["ratings"] = pd.to_numeric(all_recs["ratings"], errors="coerce")
    all_recs = all_recs[all_recs["ratings"] > 0]

    all_recs["score"] = all_recs["book_count"] * (all_recs["book_count"] / all_recs["ratings"])
    all_recs = all_recs[~all_recs["book_id"].isin(liked_books)]
    all_recs = all_recs.sort_values("score", ascending=False)

    return all_recs.head(top_n)[["book_id", "title", "score", "url", "cover_image"]].to_dict(orient="records")
