import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    if resp.status == 200:
        print(f"{url} is OK.")
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        # Find all anchor tags (hyperlinks)
        anchor_tags = soup.find_all('a', href = True)
        # Extract the href attribute from each anchor tag
        hyperlinks = []
        for link in anchor_tags:
            abs_url = urljoin(url, link.get('href'))
            final_url = urlparse(abs_url)._replace(fragment="").geturl()
            if (is_valid(final_url)) :
                hyperlinks.append(final_url)
        return hyperlinks
    else:
        print(f"{url} has {resp.error}")
        return []

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
         # Extract the hostname from the parsed URL
        hostname = parsed.hostname
        
        allowed_hostnames = r"(?:ics|cs|informatics|stat)\.uci\.edu$"
        
        # Use re.match to check if the hostname matches the domain pattern
        if re.search(allowed_hostnames, hostname): 
            return not re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
        return False

    except TypeError:
        print ("TypeError for ", parsed)
        raise
