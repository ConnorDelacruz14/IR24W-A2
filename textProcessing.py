import sys, re

# O(n) time complexity where n is the number of characters because the function gets each line 1 by 1 and goes through each character and if it is a non alphanumeric then split or continue adding the char to the current token. 

def tokenize(text):
    #try: 
    #    f = open(filename)
    #except FileNotFoundError: 
    #    print("FileNotFoundError")
    #    return
    #line = text.readline()
    token_list = []
    word = ""
    #while line != "": 
    for c in text: 
        search_char = re.search('[A-Za-z0-9]', c) 
        if search_char != None: 
            word += search_char.group(0) 
        else:
            if word != "": 
                token_list.append(word.lower())
            word = ""
    #line = f.readline()
    #print(token_list)
    return token_list


# O(n) where n is the number of tokens time complexity as it goes through each token and puts it in the dict or increases its count by 1. 

def computeWordFrequencies(token_list):
    token_dict = {}
    stopwords_f = open('stopwords.txt', 'r')
    stopwords_text = stopwords_f.read() 
    for token in token_list:
        if token not in stopwords_text:
            token_dict[token] = token_dict.get(token, 0) + 1
    #print(token_dict)
    return token_dict


#O(nlogn) time complexity where n is the number of tokens because sorting the token dict takes O(nlogn) and looping through the sorted dict and printing is O(n). So then O(nlogn + n) becomes O(nlogn). 

def printFrequencies(token_map):
    #sorted has a time complexity of O(nlogn) where n would be the number of tokens
    token_map = sorted(token_map.items(), key = lambda x: (-x[1], x[0]))
    for token, count in token_map:
        print(f'{token} -> {count}')
    #print(token_map)
    #print(len(token_map))


def intersection(): #Part B
    #O(n + m + max(m,n)) where n is the number of tokens in A and m is the number of tokens in B, because tokenizing and creating a token dict 
    #for each is linear time. Then I am looping through 1 dict and checking if each key is in the other dictionary which is max(m,n) 
    #because checking if a value is in a dict is O(1), and we are looping through all the keys in 1 dict. 

    input_list = sys.argv
    #print(input_list)

    if len(input_list) > 3: 
        raise ValueError("Too many inputs")
    elif len(input_list) < 3: 
        raise ValueError("Too few inputs")


    inf1 = A.tokenize(input_list[1])
    inf1_dict = A.computeWordFrequencies(inf1)

    inf2 = A.tokenize(input_list[2])
    inf2_dict = A.computeWordFrequencies(inf2)
    
    # O(max(n,m)) time complexity where n is the number of tokens in first dict and m is the number of tokens in second     dict. This is because we are looping through 1 dict where either dict could have more tokens and then checking it it    is in the other dict is O(1) time.   
    count = 0 
    for key in inf1_dict: 
        if key in inf2_dict: 
            count += 1

    print(count)



# O(nlogn) time complexity to call all 3 functions because tokenizing it, and creating a token_dict is O(n) each and printing it is O(nlogn) becase we sort it first. So O(n + n + nlogn) becomes O(nlogn) 

if __name__ == "__main__":
    input_list = sys.argv
    if len(input_list) > 2: 
        raise ValueError('Too many inputs.')
    elif len(input_list) < 2: 
        raise ValueError('Too few inputs.')
    
    token_list = tokenize(input_list[1])
    if token_list == None:
        raise ValueError("token_list is None")
    token_dict = computeWordFrequencies(token_list)
    printFrequencies(token_dict)
