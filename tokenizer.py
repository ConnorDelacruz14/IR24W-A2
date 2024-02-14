import re


def tokenize(lines: list) -> list:
    """
        Reads in a text file and returns a list of the tokens in that file.

        This function runs in O(n log n) time, where n is the number of words in the file.
        Putting the tokens into a list will take O(n) time, for looping over n words in the file.
        Python builtin sorted() function will run in O(n log n) time using Timsort.
    """
    tokens = []

    try:
        for line in lines:
            line_tokens = re.findall(r'[a-zA-Z0-9]+', line.lower())
            for token in line_tokens:
                tokens.append(token)

    except Exception as e:
        raise e

    return tokens


def compute_word_frequencies(tokens: list[str]) -> dict:
    """
        Counts the number of occurrences of each token in the token list.

        This function will run in O(n * m) time, where n is the number of tokens in the parameter list and
        m is the number of words in the frequencies dictionary.
        for n tokens, each token is checked with the m words in the frequencies dictionary, resulting in n * m complexity.
    """
    frequencies = {}
    for token in tokens:
        if token in frequencies.keys():
            frequencies[token] += 1
        else:
            frequencies.update({token: 1})

    return frequencies


def print_frequencies(frequencies: dict) -> dict:
    """
        returns the word frequency count onto the screen, ordered by
        decreasing frequency (highest frequencies first, ties handled alphabetically).

        This function runs in O(n log n) time, where n is the number of items in the frequencies dictionary.
        Python builtin sorted() function will run in O(n log n) time using Timsort;
        for n word and frequency pairs in the sorted dictionary, each word and frequency is printed to output.
    """
    return {key: value for key, value in sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))}

def intersection(text1, text2):
    tokenlist1 = tokenize(text1)
    tokenlist2 = tokenize(text2) 

    tokendict1 = compute_word_frequencies(tokenlist1)
    tokendict2 = compute_word_frequencies(tokenlist2)

    count = 0 
    for key in tokendict1: 
        if key in tokendict2: 
            count += 1

    return count/(max(len(tokendict1), len(tokendict2)))


def internal_comparison(lst):
    for i in range(len(lst)): 
        new_list = []
        for j in range(i+1, len(lst) - 1):
            
            if lst[i] not in new_list:
                new_list.add(lst[i])
            
            if intersection(lst[i][1], lst[j][1]) < 0.95:
                new_list.add(lst[j])
            
        lst = new_list
    return lst

def simhash(token_dict): 
    hash_values = []
    hash_values_len = [] 
    for word in token_dict: 
        lst = ""
        for c in word: 
            val = format(ord(c), 'd')
            if int(val) > 110: 
                lst += "1"
            else:
                lst += "0"
        
        hash_values.append((lst,word))
        hash_values_len.append(len(lst))
    min_size = min(hash_values_len)


    vector_vals = [0] * min_size
    for i in range(len(vector_vals)): #for every vector index
        #print(f'i is {i}')
        for index, tple in enumerate(hash_values): #for every word 
            #print(f'index is {index} and word is {tple}')
            binary_value = tple[0] 
            word = tple[1] 
            #print(f'index is {index}')
            #print(f'binary_value is {binary_value} and value at index {i} is {binary_value[i]} and value is {token_dict[word]}')
            if binary_value[i] == '0':
                vector_vals[i] -= token_dict[word]
            elif binary_value[i] == '1':
                vector_vals[i] += token_dict[word]

            print(vector_vals)

    ret = ""
    for i in vector_vals:
        if i >= 0:
            ret += '1'
        else:
            ret += '0'
    
    return ret


def simhash_comparison(s1, s2):
    min_len = min(len(s1), len(s2))
    max_len = max(len(s1), len(s2))
    count_similar_bits = 0
    for i in range(min_len):
        if s1[i] == s2[i]:
            count_similar_bits += 1
    
    return count_similar_bits/max_len

    

def checksum(text):
    s = 0
    for c in text: 
        character = ord(c)
        print(f'character is {character}')
        s += character
    print(f'sum is {hex(s)}')
    

if __name__ == '__main__':
    dictionary = {"hello" : 1, "by2" : 1, "firefly": 2}
    print(simhash(dictionary))
    #print(simhash_comparison("111111", "00011111110000000000000"))







    