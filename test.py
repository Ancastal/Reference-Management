import requests
from bs4 import BeautifulSoup

def search_google_scholar(title):
    # Format the search query
    query = '+'.join(title.split())

    import requests, random

    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    for _ in user_agent_list:
    #Pick a random user agent
        user_agent = random.choice(user_agent_list)

    #Set the headers
    headers = {'User-Agent': user_agent}
    session = requests.Session()
    session.headers['User-Agent'] = random.choice(user_agent_list)

    # Send a GET request to the Google Scholar search page

    # Send a GET request to the Google Scholar search page
    url = f'https://scholar.google.com/scholar?q={query}'
    response = session.get(url)

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())
    # Find the desired search result element

    # Extract the title and URL of the first result
    title = soup.find('h3', {'class': 'gs_rt'})
    div = soup.select_one('#gs_res_ccl_mid > div:nth-child(1) > div.gs_ggs.gs_fl > div > div')
    pdf_url = div.find('a', href=True)['href']
    if title and pdf_url:
        return title, pdf_url
    else:
        return None

def download_pdf(title, url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    with open(f'{title}.pdf', 'wb') as file:
        file.write(response.content)

def extract_abstract(text):
    # Split the text into paragraphs
    paragraphs = text.split('\n')

    # Find the paragraph(s) containing the abstract
    abstract_paragraphs = []
    capturing_abstract = False
    for paragraph in paragraphs:
        stripped_paragraph = paragraph.strip()
        if stripped_paragraph.lower().startswith('abstract'):
            abstract_paragraphs.append(stripped_paragraph)
            capturing_abstract = True
        elif capturing_abstract and stripped_paragraph:
            abstract_paragraphs.append(stripped_paragraph)
        elif capturing_abstract and not stripped_paragraph:
            break

    # Extract the abstract text
    if abstract_paragraphs:
        abstract = ' '.join(abstract_paragraphs)
        abstract = abstract.replace('Abstract', '').strip()
        return abstract
    else:
        return None

# Example usage
title = 'A Deep Reinforcement Learning Chatbot'
result = search_google_scholar(title)
if result:
    print(f"Title: {result[0]}")
    print(f"PDF URL: {result[1]}")
    # Download the PDF file
    download_pdf(result[0], result[1])
    import pypdf
    pdf = pypdf.PdfReader(f'{result[0]}.pdf')
    for page in pdf.pages:
        if 'abstract' in page.extract_text().lower() and '.................................................' not in page.extract_text().lower():
            text = page.extract_text().split('Abstract')[1]
            break
    print(text)

else:
    print("No results found.")
