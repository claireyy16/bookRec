import type { Book } from "../types/bookType";

type Props = {
  results: Book[];
  onReset: () => void;
};

export default function ResultsPage({ results, onReset }: Props) {
  return (
    <div>
      <button onClick={onReset}>🔙 Home</button>
      <ul>
        {results.map((book, i) => (
          <li key={i}>
            <strong>{book.title}</strong> — {book.ratings} ratings <br />
            <a href={book.url} target="_blank" rel="noreferrer">Goodreads</a><br />
            <img src={book.cover_image} alt={book.title} width={50} />
          </li>
        ))}
      </ul>
    </div>
  );
}
