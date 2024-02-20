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
            if len(tokens) > 10000:
                return []
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

