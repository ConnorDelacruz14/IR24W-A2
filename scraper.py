import re
from parser import Parser
from urllib.parse import urlparse

ALLOWED_DOMAINS = [
    'ics.uci.edu',
    'cs.uci.edu',
    'informatics.uci.edu',
    'stat.uci.edu'
]
SIMILARITY_THRESHOLD = 0.95

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
        return list()

    extractor = Parser(url, resp.raw_response.content)
    page_tokens = extractor.tokenize_web_text()
    if (len(page_tokens)) < 100:
        return list()

    Parser.all_tokens.extend(page_tokens)

    extractor.update_unique_pages()
    extractor.update_subdomain()

    fingerprint = simhash(extractor.get_word_frequencies())
    print("Fingerprint:", fingerprint)
    for existing_fingerprint in Parser.fingerprints:
        similarity = simhash_bit_comparison(fingerprint, existing_fingerprint)
        if similarity >= SIMILARITY_THRESHOLD:
            print(f"Fingerprint is too similar to an existing one: {existing_fingerprint} "
                  f"with similarity of {similarity * 100}%")
            return list()

    Parser.fingerprints.add(fingerprint)

    return extractor.get_links_from_webpage()


def simhash(tokens, max_hash_bits=64):
    vector_vals = [0] * max_hash_bits
    for token in tokens:
        # Generate a basic hash of the token
        hash_value = 0
        for char in token:
            hash_value = (hash_value * 31 + ord(char)) % (2 ** max_hash_bits)

        for i in range(max_hash_bits):
            bitmask = 1 << i
            if hash_value & bitmask:
                vector_vals[i] += 1
            else:
                vector_vals[i] -= 1

    # Create the fingerprint
    fingerprint = 0
    for i in range(max_hash_bits):
        if vector_vals[i] >= 0:
            fingerprint |= (1 << i)
    return bin(fingerprint)[2:]


def simhash_bit_comparison(s1, s2):
    min_len = min(len(s1), len(s2))
    max_len = max(len(s1), len(s2))
    count_similar_bits = 0
    for i in range(min_len):
        if s1[i] == s2[i]:
            count_similar_bits += 1

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

        if parsed.scheme not in {"http", "https"}:
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|txt|ppsx|nb|r|img|war|json"  # we added these
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
