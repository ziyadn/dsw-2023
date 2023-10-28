import re

def ngrams(string, n=3):
    string = string.lower()
    string = re.sub(r'[,-./]|\sBD', '', string)
    ngrams = zip(*[string[i:] for i in range(n)])

    return [''.join(ngram) for ngram in ngrams]