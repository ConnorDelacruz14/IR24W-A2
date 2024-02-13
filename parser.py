import tokenizer
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class Parser:
    pages_parsed = 0
    unique_pages = 0
    all_tokens = 0     # ignoring english stopwords
    longest_page = {}  # {"URL": total_words}
    subdomains = {}    # {"http://vision.ics.uci.edu": 10}
    politeness = {}    # information of robots.txt

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

    def get_politeness_information(self) -> dict:
        '''
        Input: none
        Returns: a dictionary that contains allowed paths, disallowed paths, and the sitemap 
        '''
        parsed_url = urlparse(self.url)
        main_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        if main_url not in politeness:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            robot_path = f"{main_url}/robots.txt"
            robot_content = requests.get(robot_path, verify=False).text.split('\n')
            parsed_dict = {'Allow':[], 'Disallow':[], 'Sitemap':''}
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
            politeness[main_url] = parsed_dict
            return parsed_dict
        else:
            return politeness[main_url]

    def tokenize_web_text(self) -> list:
        page_text = self.soup.get_text()
        self.tokens = tokenizer.tokenize([line.strip() for line in page_text.split('\n') if line.strip()],
                                         stopwords=True)

        return self.tokens
    