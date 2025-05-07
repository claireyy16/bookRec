from flask import Flask, jsonify, request
from data_processing import load_and_prepare, search_books, recommend_books

app = Flask(__name__)
load_and_prepare()

@app.route("/api/search")
def search_api():
    query = request.args.get("q", "")
    if not query.strip():
        return jsonify({"error": "Missing search query (?q=...)"})
    results = search_books(query)
    return jsonify(results)

@app.route("/api/recommend", methods=["POST"])
def recommend_api():
    data = request.get_json()
    liked_books = data.get("liked_books", [])
    top_n = int(data.get("top_n", 10))

    if not liked_books or not isinstance(liked_books, list):
        return jsonify({"error": "Send JSON with 'liked_books': [list of book_ids]"}), 400

    recommendations = recommend_books(liked_books, top_n=top_n)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
