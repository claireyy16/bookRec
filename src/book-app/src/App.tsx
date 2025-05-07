import { useState } from "react";
import { searchBooks } from "./api";
import type { Book } from "./types/bookType";
import SearchPage from "./components/SearchPage";
import ResultsPage from "./components/ResultsPage";

function App() {
  const [results, setResults] = useState<Book[]>([]);
  const [view, setView] = useState<"home" | "results">("home");

  const handleSearch = async (query: string) => {
    const data = await searchBooks(query);
    setResults(data);
    setView("results");
  };

  const handleReset = () => {
    setResults([]);
    setView("home");
  };

  return (
    <div style={{ padding: "1rem" }}>
      {view === "home" ? (
        <SearchPage onSearch={handleSearch} />
      ) : (
        <ResultsPage results={results} onReset={handleReset} />
      )}
    </div>
  );
}

export default App;
