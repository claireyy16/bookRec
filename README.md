## About

Book recommendation search engine based off UCSD datasets from goodreads, using Python scripts in Jupyter Notebook, pandas, numpy, scikit-learn, vectorizers, etc.

> Note: goodreads API has since been retired, these datasets are a couple years old

Users can use this search engine to look for a book's information using the search engine, or input a list of books that they like and find tailored recommendations from other users with similar taste. 

The script reads in data from the datasets and normalizes the data so the search engine is more efficient. 

Using the [scikit-learn Tfidf Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), we use the inverse frequency matrix to determine importance of search words

## Examples
Easier to see in 'recommendations.ipynb' and 'search.ipynb' files

#### Using search engine:
![image](https://github.com/user-attachments/assets/2d6a7b03-9b40-4e6d-a3ca-cde41789e200)


#### Finding recommended books:
![image](https://github.com/user-attachments/assets/ca6f5034-4283-4756-9f50-760a1045f7df)

## Next Steps
I'm hoping to get time to make a frontend for this after finals ends


## Data Sets Used:

goodreads_interactions.csv: user_id, book_id, and rating for each book
goodreads_books.json.gz: individual book metadata
book_id_map.csv: book_id map to associate ids across the two previous datasets

Information from https://cseweb.ucsd.edu/~jmcauley/datasets/goodreads.html

## Citations:
Followed guidance from DataQuest on [YouTube](https://youtu.be/x-alwfgQ-cY?si=w4q2eiOomHXJux1a)

Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.  [bibtex]

Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19. [bibtex]
