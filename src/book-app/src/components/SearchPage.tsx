import { useState } from "react";

type Props = {
  onSearch: (query: string) => void;
};

export default function SearchPage({ onSearch }: Props) {
  const [query, setQuery] = useState("");

  return (
    <div>
      <h1>Book Search</h1>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search books..."
      />
      <button onClick={() => onSearch(query)}>Search</button>
    </div>
  );
}
