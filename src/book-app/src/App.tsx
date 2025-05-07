import { useState } from "react";
import { searchBooks, recommendBooks } from "./api";
import { type Book } from "./types/bookType";


function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Book[]>([]);

  const handleSearch = async () => {
    const data = await searchBooks(query);
    setResults(data);
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h1>Book Search</h1>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search books..."
      />
      <button onClick={handleSearch}>Search</button>

      <ul>
        {results.map((book, i) => (
          <li key={i}>
            <strong>{book.title}</strong> — {book.ratings} ratings <br />
            <a href={book.url} target="_blank">Goodreads</a>
            <br />
            <img src={book.cover_image} alt={book.title} width={50} />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
