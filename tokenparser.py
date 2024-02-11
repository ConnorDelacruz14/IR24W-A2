class Parser(): 
    global unique_pages 
    unique_pages = 0 
    global unique_pages_set 
    unique_pages_set = set()
    longest_page = None
    longest_page_count = 0
    common_words = dict() 
    subdomain = [] 

    def __init__(self, url = None, token_list = None , token_dict = None):
        if url != None: 
            self.update_uniquePages(url)
            self.update_longest_page(token_list)
            self.update_common_words(token_dict)

    def update_uniquePages(self, url):
        if url not in unique_pages_set:
            unique_pages += 1
            unique_pages_set.add(url)

    def update_longest_page(self, token_list):
        if len(token_list) > longest_page_count: 
            longest_page = url 
            longest_page_count = len(token_list)
    
    
    # at the end of running this scraper we should get 50
    def update_common_words(self):
        for word in common_words: 
            if word in common_words: 
                common_words[word] += 1
            else:
                common_words[word] = 1



def initialize(): 
    global parser_var
    parser_var = Parser()      