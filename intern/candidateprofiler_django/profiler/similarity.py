from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score

def fuzzy_match(a, b):
    return fuzz.ratio(a.lower(), b.lower())

def jaccard_sim(a, b):
    vect = CountVectorizer(binary=True)
    vecs = vect.fit_transform([a, b])
    return jaccard_score(vecs.toarray()[0], vecs.toarray()[1])
