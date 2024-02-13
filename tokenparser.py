import re
class Parser(): 
    unique_pages = 0  
    unique_pages_set = set()
    longest_page = None
    longest_page_count = 0
    common_words = dict() 
    subdomain = dict()

    def __init__(self, url = None, token_list = None , token_dict = None):
        self.update_uniquePages(url)
        self.update_longest_page(url, token_list)
        self.update_common_words(token_dict)
        self.update_subdomain(url)

    def update_uniquePages(self, url):
        if url not in self.unique_pages_set:
            Parser.unique_pages_set.add(url)
            #print(f'unique_pages is {self.unique_pages}')
            Parser.unique_pages += 1

    def update_longest_page(self, url, token_list):
        if len(token_list) > self.longest_page_count: 
            Parser.longest_page = url 
            Parser.longest_page_count = len(token_list)
    
    
    # at the end of running this scraper we should get 50
    def update_common_words(self, token_dict):
        for word in token_dict: 
            if word in self.common_words: 
                Parser.common_words[word] += token_dict[word]
            else:
                Parser.common_words[word] = token_dict[word]

    def update_subdomain(self, url): 
        sub = re.match(r'^.*\.ics.uci.edu', url)
        if sub != None:
            word = sub.group(0)
            if word in self.subdomain: 
                Parser.subdomain[word] += 1
            else:
                Parser.subdomain[word] = 1

    