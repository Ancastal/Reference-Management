import gensim
from pybibtex import BibTeXFile
from gensim import corpora, models

# Load database
DATABASE_FILE = 'references.bib'
database = BibTeXFile(DATABASE_FILE)

# Prepare data for LDA
documents = [entry.fields.get('title', '') for entry in database.entries.values()]

# Preprocess data
texts = [[word for word in document.lower().split()] for document in documents]

# Create a Gensim dictionary from the texts
dictionary = corpora.Dictionary(texts)

# Remove extremes (similar to the min/max df step used when creating the tf-idf matrix)
dictionary.filter_extremes(no_below=1, no_above=0.8)

# Convert the dictionary to a bag of words corpus for reference
corpus = [dictionary.doc2bow(text) for text in texts]

# Initialize an LDA model
lda = models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=50)

def suggest_related(keyword):
    # Search for the key that matches the keyword
    matching_keys = [key for key, entry in database.entries.items() if keyword.lower() in entry.fields.get('title', '').lower()]
    if not matching_keys:
        print("No matching references found.")
        return

    # Get the first matching key
    key = matching_keys[0]

    # Get the document's bag-of-words representation
    doc_bow = dictionary.doc2bow(database.entries[key].fields.get('title', '').lower().split())

    # Get the document's topic distribution
    doc_lda = lda[doc_bow]

    # Get the topic distributions for all documents
    all_lda = lda[corpus]

    # Find the documents with the most similar topic distributions
    similar_docs = sorted(enumerate(all_lda), key=lambda item: gensim.matutils.cossim(doc_lda, item[1]), reverse=True)

    print("Most similar references to: ", key)
    for doc_index, similarity in similar_docs[:5]:  # Show top 5
        doc_key = list(database.entries.keys())[doc_index]
        print(database.entries[doc_key].generate_citation())
