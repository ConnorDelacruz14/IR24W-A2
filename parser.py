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
    URL_counter = {}
    fingerprints = set()

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
            # Reconstruct the URL without the fragment and path
            bare_url = parsed_url._replace(fragment="", query="").geturl()
            # Crawler trap detection
            if str(bare_url) not in self.URL_counter:
                Parser.URL_counter[str(bare_url)] = 1
            else:
                Parser.URL_counter[str(bare_url)] = 1

            if Parser.URL_counter[str(bare_url)] < 3:
                self.page_links.append(bare_url)

        return self.page_links

    def tokenize_web_text(self) -> list:
        page_text = self.soup.get_text()
        self.tokens = tokenizer.tokenize([line.strip() for line in page_text.split('\n') if line.strip()])
        if len(self.tokens) > Parser.longest_page[1]:
            Parser.longest_page = (self.url, len(self.tokens))
        return self.tokens

    def get_word_frequencies(self) -> dict:
        return tokenizer.compute_word_frequencies(self.tokens)

    def update_unique_pages(self) -> None:
        if self.url not in self.unique_pages:
            Parser.unique_pages.add(self.url)

    def update_subdomain(self) -> None:
        match = re.search(r'(?<=://)?([a-zA-Z0-9.-]+)\.ics\.uci\.edu', self.url)
        if match is not None:
            domain = match.group(1) + '.ics.uci.edu'
            if domain in Parser.subdomains:
                Parser.subdomains[domain] += 1
            else:
                Parser.subdomains[domain] = 1

    def simple_hash(self, token, hash_bits=64):
        """A very basic hashing function."""
        hash = 0
        for char in token:
            hash = (hash * 31 + ord(char)) % (2 ** hash_bits)
        return hash

    def simhash(self, tokens, hash_bits=128):
        v = [0] * hash_bits
        for token in tokens:
            # Generate a basic hash of the token
            hash = self.simple_hash(token, hash_bits)
            for i in range(hash_bits):
                bitmask = 1 << i
                if hash & bitmask:
                    v[i] += 1
                else:
                    v[i] -= 1
        # Create the fingerprint
        fingerprint = 0
        for i in range(hash_bits):
            if v[i] >= 0:
                fingerprint |= (1 << i)
        return fingerprint

    def hamming_distance(self, f1, f2):
        x = f1 ^ f2
        total = 0
        while x:
            total += 1
            x &= x - 1
        return total

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
        print("Top 50 word frequencies:")
        _count = 0
        for word, frequency in Parser.get_all_word_frequencies().items():
            if _count < 50:
                print(word, frequency)
                _count += 1
            else:
                break
        print("Total pages parsed:", Parser.pages_parsed)
        print(f"Unique pages: {len(Parser.unique_pages)}")
        print(f"Longest page was {Parser.get_longest_page()[0]} with {Parser.get_longest_page()[1]} words")
        print(".ics.uci.edu Subdomains:", Parser.subdomains)
