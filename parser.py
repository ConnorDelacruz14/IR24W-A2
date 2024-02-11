import tokenizer
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class Parser:
    pages_parsed = 0
    unique_pages = 0
    all_tokens = 0     # ignoring english stopwords
    longest_page = {}  # {"URL": total_words}
    subdomains = {}    # {"http://vision.ics.uci.edu": 10}

    def __init__(self, url: str, content: str) -> None:
        Parser.pages_parsed += 1
        self.url = url
        self.content = content
        self.page_links = []
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.tokens = []

    def get_links_from_webpage(self) -> list:
        for link in self.soup.find_all('a', href=True):
            href = link.get('href')
            # Create an absolute URL from a possible relative URL and the base URL
            absolute_url = urljoin(self.url, href)
            parsed_url = urlparse(absolute_url)
            # Reconstruct the URL without the fragment
            defragmented_url = parsed_url._replace(fragment="").geturl()
            self.page_links.append(defragmented_url)

        return self.page_links

    def tokenize_web_text(self) -> list:
        page_text = self.soup.get_text()
        self.tokens = tokenizer.tokenize([line.strip() for line in page_text.split('\n') if line.strip()],
                                         stopwords=True)

        return self.tokens
