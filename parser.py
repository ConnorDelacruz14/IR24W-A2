import tokenizer
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class Parser:
    pages_parsed = 0
    unique_pages = set()
    all_tokens = []
    all_frequencies = {}  # all frequencies of words ignoring english stopwords
    longest_page = ("", 0)  # {"URL": total_words}
    subdomains = {}  # {"http://vision.ics.uci.edu": 10}

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
        self.tokens = tokenizer.tokenize([line.strip() for line in page_text.split('\n') if line.strip()])
        if len(self.tokens) > Parser.longest_page[1]:
            Parser.longest_page = (self.url, len(self.tokens))
        return self.tokens

    def get_word_frequencies(self) -> dict:
        return tokenizer.compute_word_frequencies(self.tokens)

    def update_unique_pages(self):
        if self.url not in self.unique_pages:
            Parser.unique_pages.add(self.url)

    def update_subdomain(self):
        sub = re.match(r'^.*\.ics.uci.edu', self.url)
        if sub is not None:
            word = sub.group(0)
            if word in Parser.subdomains.items():
                Parser.subdomains[word] += 1
            else:
                Parser.subdomains[word] = 1

    @staticmethod
    def get_all_word_frequencies() -> dict:
        with open("stopwords.txt", 'r') as stopwords_file:
            stopwords = set(word.strip() for word in stopwords_file.readlines())
            word_frequencies = tokenizer.compute_word_frequencies(Parser.all_tokens)
            sorted_frequencies = tokenizer.print_frequencies(word_frequencies)
            return {word: frequency for word, frequency in sorted_frequencies.items() if word not in stopwords}

    @staticmethod
    def get_subdomains() -> dict:
        return Parser.subdomains

    @staticmethod
    def get_longest_page() -> dict:
        return Parser.longest_page

    @staticmethod
    def print_crawler_report() -> None:
        print("Total pages parsed:", Parser.pages_parsed)
        print(f"Unique pages: {len(Parser.unique_pages)}")
        print("All word frequencies:")
        for word, count in Parser.get_all_word_frequencies().items():
            print(word, count)
        print(f"Longest page was {Parser.get_longest_page()[0]} with {Parser.get_longest_page()[1]} words")
        print("Subdomains:", Parser.subdomains)
