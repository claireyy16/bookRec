##About

Book recommendation search engine based off UCSD datasets from goodreads, using Python scripts in Jupyter Notebook, pandas, numpy, scikit-learn, vectorizers, etc.

> Note: goodreads API has since been retired, these datasets are a couple years old

Users can use this search engine to look for a book's information using the search engine, or input a list of books that they like and find tailored recommendations from other users with similar taste. 

The script reads in data from the datasets and normalizes the data so the search engine is more efficient. 

Using the [scikit-learn Tfidf Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), we use the inverse frequency matrix to determine importance of search words

##Examples

Using search engine:

Finding recommended books:

##Data Sets Used:

goodreads_interactions.csv: user_id, book_id, and rating for each book
goodreads_books.json.gz: individual book metadata
book_id_map.csv: book_id map to associate ids across the two previous datasets

Information from https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html

##Citations:
Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.  [bibtex]

Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19. [bibtex]
