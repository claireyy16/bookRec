const BASE_URL = "http://127.0.0.1:5000/api";

export async function searchBooks(query: any) {
  const res = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(query)}`);
  return res.json();
}

export async function recommendBooks(likedBooks: any, topN = 5) {
  const res = await fetch(`${BASE_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ liked_books: likedBooks, top_n: topN }),
  });
  return res.json();
}
