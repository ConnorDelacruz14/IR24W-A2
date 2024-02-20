import re
from parser import Parser
from urllib.parse import urlparse

ALLOWED_DOMAINS = [
    'ics.uci.edu',
    'cs.uci.edu',
    'informatics.uci.edu',
    'stat.uci.edu'
]

SIMILARITY_THRESHOLD = 0.95  # Threshold for checking the similarity between two pages


# Parameters: url, resp
# Returns each valid link that is present on the current webpage
def scraper(url, resp) -> list:
    return [link for link in extract_next_links(url, resp) if is_valid(link)]


def extract_next_links(url, resp) -> list:
    # Implementation required. url: the URL that was used to get the page resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there
    # was some kind of problem. resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    # resp.raw_response.url: the url, again resp.raw_response.content: the content of the page! Return a list with
    # the hyperlinks (as strings) scrapped from resp.raw_response.content
    """
        Input: url and resp object
        Returns a list of hyperlinks from the url
    """
    if resp.status != 200:
        return list()

    # Create new Parser for this webpage and extract the tokens from it
    extractor = Parser(url, resp.raw_response.content)
    page_tokens = extractor.tokenize_web_text()

    # Ignores url that has less than 100 tokens
    if (len(page_tokens)) < 100:
        return list()

    Parser.all_tokens.extend(page_tokens)

    extractor.update_unique_pages()
    extractor.update_subdomain()

    # EXTRA CREDIT +2 POINTS
    # Performs check on similar websites based on their tokens using simhash algorithm from class
    # Current threshold is stored in SIMILARITY_THRESHOLD global variable
    fingerprint = simhash(page_tokens)

    for existing_fingerprint in Parser.fingerprints:
        similarity = simhash_bit_comparison(fingerprint, existing_fingerprint)
        if similarity >= SIMILARITY_THRESHOLD:
            return list()

    Parser.fingerprints.add(fingerprint)

    return extractor.get_links_from_webpage()


def simhash(tokens: list, max_hash_bits=64) -> str:
    """
        Input: token list and max_hash_bits value
        Returns the fingerprint value based
    """
    vector_vals = [0] * max_hash_bits  # max length of vector is 64 bits (word length no less than that)
    for token in tokens:
        # Create a basic hash of each token

        hash_value = 0
        for char in token:
            # multiply the hash value by 31,
            # add the ASCII value of the character
            # modulo the result by 2 to power of max_hash_bits to limit the hash_value
            hash_value = (hash_value * 31 + ord(char)) % (2 ** max_hash_bits)

        # generate the vector values iterate through every bit and for the current token if the hash bit value is 1
        # we increase the sum at vector_vals by 1 else decrease by 1
        for i in range(max_hash_bits):
            bitmask = 1 << i
            if hash_value & bitmask:
                vector_vals[i] += 1
            else:
                vector_vals[i] -= 1

    # Create the fingerprint for identifying a webpage
    # If the ith component of the vector is positive, the fingerprint's ith bit is set to 1
    # otherwise it remains 0
    fingerprint = 0
    for i in range(max_hash_bits):
        if vector_vals[i] >= 0:
            fingerprint |= (1 << i)

    return bin(fingerprint)[2:]  # bin() returns a string "0b....." -> slicing gets rid of that


def simhash_bit_comparison(s1: str, s2: str) -> float:
    """
        Input: binary strings
        Returns the percentage of similar bits between the binary numbers.
    """
    min_len = min(len(s1), len(s2))
    max_len = max(len(s1), len(s2))
    count_similar_bits = 0

    # Count the number of bits that are the same for the binary strings
    for i in range(min_len):
        if s1[i] == s2[i]:
            count_similar_bits += 1

    # Calculate similarity percentage
    return count_similar_bits / max_len


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

        # Avoiding URLS with these file types
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|txt|ppsx|nb|r|img|war|json|pps"  # we added these
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
