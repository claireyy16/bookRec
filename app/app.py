from flask import Flask, jsonify, request
from searchPy import load_and_prepare, search_books, recommend_books
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

try:
    print("Loading data...")
    from searchPy import load_and_prepare

    load_and_prepare(
        book_path="goodreads_books.json.gz",
        id_map_path="book_id_map.csv",
        interactions_path="goodreads_interactions.csv"
)    
    print("Data loaded.")
except Exception as e:
    print("Failed to load data:", e)
    
@app.route("/debug/routes")
def list_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])
    
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
    app.run(host="127.0.0.1", port=5000, debug=True)
