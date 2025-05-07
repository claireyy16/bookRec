export type Book = {
  title: string;
  ratings: number;
  url: string;
  cover_image: string;
  book_id?: string; // optional, useful for recommendations
  score?: number;   // optional, if showing score in recommendations
};