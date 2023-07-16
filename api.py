import arxiv
from collections import Counter
from pypdf import PdfReader



# Use the function to extract references from a PDF
# nlp = spacy.load("en_core_web_sm")

# Search for articles by the desired author
def search_title(title):
    author_query = arxiv.Search(query=f"ti:\"{title}\"", max_results=1)

    for result in author_query.results():
        print(result.summary)



def search_author(author):
    author_query = arxiv.Search(query=f"au:\"{author}\"", max_results=1)

    for result in author_query.results():
        source = result.download_pdf()
        pdf = PdfReader(source)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        print(text)

def search_abstract(abstract):
    author_query = arxiv.Search(query=f"abs:\"{abstract}\"", max_results=1)

    for result in author_query.results():
        print(result.summary)

def search_category(category):
    author_query = arxiv.Search(query=f"cat:\"{category}\"", max_results=1)

    for result in author_query.results():
        source = result.download_pdf()
        pdf = PdfReader(source)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        print(text)

def search_keyword(keyword):
    author_query = arxiv.Search(query=f"all:\"{keyword}\"", max_results=1)

    for result in author_query.results():
        source = result.download_pdf()
        pdf = PdfReader(source)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        print(text)

def extract_references(text):
    # Extract the references from the text
    references = []
    for line in text.splitlines():
        if line.startswith("["):
            references.append(line)
    return references

def count_references(references):
    # Count the references
    counts = Counter(references)
    return counts

def get_reference_by_title(title):
    # Search for articles by the desired author
    author_query = arxiv.Search(query=f"ti:\"{title}\"", max_results=1)

    for result in author_query.results():
        source = result.download_pdf()
        pdf = PdfReader(source)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

search_title("Workshop on Computational linguistics for Literature Towards a Literary Machine Translation: The Role of Referential Cohesion")
