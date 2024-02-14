import re
from parser import Parser
from urllib.parse import urlparse

ALLOWED_DOMAINS = [
    'ics.uci.edu',
    'cs.uci.edu',
    'informatics.uci.edu',
    'stat.uci.edu'
]


def scraper(url, resp):
    return [link for link in extract_next_links(url, resp) if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required. url: the URL that was used to get the page resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there
    # was some kind of problem. resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    # resp.raw_response.url: the url, again resp.raw_response.content: the content of the page! Return a list with
    # the hyperlinks (as strings) scrapped from resp.raw_response.content
    if resp.status != 200:
        print(f"Error code {resp.status}")
        return list()

    extractor = Parser(url, resp.raw_response.content)
    print("Pages parsed:", Parser.pages_parsed)
    print(resp.raw_response.url)
    return extractor.get_links_from_webpage()


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        # Only allow subdomains and domains that are allowed
        domain_matches = any(domain for domain in ALLOWED_DOMAINS if parsed.netloc.endswith(domain))
        if not domain_matches:
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise