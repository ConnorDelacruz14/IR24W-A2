import tokenizer
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class Parser:
    """
        Class representing a parser for a given webpage, including static variables and methods for 
        gathering data based on every page that is parsed.
    """
    pages_parsed = 0
    unique_pages = set()
    all_tokens = []
    all_frequencies = {}  # all frequencies of words ignoring english stopwords
    longest_page = ("", 0)  # {"URL": total_words}
    subdomains = {}  # {"http://vision.ics.uci.edu": 10}
    URL_counter = {}
    fingerprints = set() # keep track of each page's fingerprint for simhashing comparisons
    politeness = {}

    def __init__(self, url: str, content: str) -> None:
        Parser.pages_parsed += 1
        self.url = url
        self.content = content
        self.page_links = []
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.tokens = []


    # EXTRA CREDIT +1 POINTS
    def get_politeness_information(self) -> dict:
        # Due to the limitation of accessing the robots.txt of each base domain directly without
        # using the cache server, we have had to download these text files to local and perform 
        # checking through them. 
        """
            Returns: a dictionary that contains allowed paths, disallowed paths, and the sitemap.
        """
        parsed_url = urlparse(self.url)
        main_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        # Check if this link's robots.txt has already been added to the dictionary for performance enhancement
        if main_url not in Parser.politeness: 
            robot_path = "DNE.txt"
            if main_url.endswith("informatics.uci.edu"): # determining what robots.txt to check based on the url
                robot_path = "./robots/informatics.txt"
            elif main_url.endswith("cs.ics.uci.edu") or main_url.endswith("cs.uci.edu"):
                robot_path = "./robots/cs.txt"
            elif main_url.endswith("ics.uci.edu"):
                robot_path = "./robots/ics.txt"
            elif main_url.endswith("stat.uci.edu"):
                robot_path = "./robots/stat.txt"
            try:
                # Reads robots.txt of the url and performs extracting disallowed links and allowed links
                # Also extracts the sitemap and outputs all of the information into a dictionary
                with open(robot_path, "r") as robot_file:
                    robot_content = robot_file.readlines()
                    parsed_dict = {'Allow': [], 'Disallow': [], 'Sitemap': ''}
                    for line in robot_content:
                        parts = line.split(' ')
                        if len(parts) >= 2:
                            value = parts[1]
                            if line.startswith('Allow:'):
                                parsed_dict['Allow'].append(f"{main_url}{value}")
                            elif line.startswith('Disallow:'):
                                parsed_dict['Disallow'].append(f"{main_url}{value}")
                            elif line.startswith('Sitemap:'):
                                parsed_dict['Sitemap'] = value
                        else:
                            continue
                    Parser.politeness[main_url] = parsed_dict
                    return parsed_dict
            except FileNotFoundError:
                print(f"{main_url} is an invalid link.")
                return {}
        else:
            return Parser.politeness[main_url]


    def get_links_from_webpage(self) -> list:
        """
            Returns a list of all the valid links from a given webpage, making sure to 
            avoid trap links and abide by politeness rules.
        """
        pln = self.get_politeness_information()
        disallowed_links = pln['Disallow']
        allowed_links = pln['Allow']
        for link in self.soup.find_all('a', href=True):
            href = link.get('href')
            # Create an absolute URL from a possible relative URL and the base URL
            absolute_url = urljoin(self.url, href)
            parsed_url = urlparse(absolute_url)
            # Reconstruct the URL without the fragment and path
            bare_url = parsed_url._replace(fragment="", query="").geturl()
            # Check Robots.txt first, if current link is disallowed, skip
            is_allowed = True
            for disallowed_link in disallowed_links:
                # Certain paths are allowed despite that they consist the disallowed portion,
                # we check if the allowed links consist the current link, then we proceed, otherwise, skip.
                if disallowed_link in bare_url and bare_url not in allowed_links:
                    is_allowed = False
            # Crawler trap detection
            if is_allowed:
                if str(bare_url) not in self.URL_counter:
                    Parser.URL_counter[str(bare_url)] = 1
                else:
                    Parser.URL_counter[str(bare_url)] += 1

                if Parser.URL_counter[str(bare_url)] < 3:
                    self.page_links.append(bare_url)
        return self.page_links


    def tokenize_web_text(self) -> list:
        """
            Returns a list of the tokens of the current web page.
        """
        page_text = self.soup.get_text()
        self.tokens = tokenizer.tokenize([line.strip() for line in page_text.split('\n') if line.strip()])
        
        # Check if this is the longest page
        if len(self.tokens) > Parser.longest_page[1]:
            Parser.longest_page = (self.url, len(self.tokens)) 
        return self.tokens


    def get_word_frequencies(self) -> dict:
        """
            Returns a dictionary that contains the word frequency information for the Parser's webpage
            with the format {"url": frequency}
        """
        return tokenizer.compute_word_frequencies(self.tokens)


    def update_unique_pages(self) -> None:
        """
            Checks if this parser's page has been looked parsed before, and updates the static set.
        """
        if self.url not in self.unique_pages:
            Parser.unique_pages.add(self.url)


    def update_subdomain(self) -> None:
        """
            Adds a new domain to the static dictionary of subdomains from this given parser object.
        """
        match = re.search(r'(?<=://)?([a-zA-Z0-9.-]+)\.ics\.uci\.edu', self.url)
        if match is not None:
            domain = match.group(1) + '.ics.uci.edu'
            if domain in Parser.subdomains:
                Parser.subdomains[domain] += 1
            else:
                Parser.subdomains[domain] = 1


    @staticmethod
    def get_all_word_frequencies() -> dict:
        """
            Returns a word frequency dictionary for all words seen so far, taking from
            the static class variable 'tokens'.
        """
        with open("stopwords.txt", 'r') as stopwords_file:
            stopwords = set(word.strip() for word in stopwords_file.readlines())
            word_frequencies = tokenizer.compute_word_frequencies(Parser.all_tokens)
            sorted_frequencies = tokenizer.print_frequencies(word_frequencies)
            return {word: frequency for word, frequency in sorted_frequencies.items() if word not in stopwords}


    @staticmethod
    def get_subdomains() -> dict:
        """
            Returns a dictionary of all ics.uci.edu subdomains that are checked with their frequencies.
        """
        return Parser.subdomains


    @staticmethod
    def get_longest_page() -> dict:
        """
            Returns a dictionary that contains the url of the a crawled page and the
            number of words in that page.
        """
        return Parser.longest_page


    @staticmethod
    def print_crawler_report() -> None:
        """
            Prints the crawler report, printing information about word frequencies,
            pages parsed, unique pages, longest page, and subdomains.
        """
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
