import pickle
import nltk

with open("middle_file/wordFreq.pickle","rb") as f:
    word_features = pickle.load(f)
with open("middle_file/classifier.pickle","rb") as cl:
    classifier = pickle.load(cl)


def tokennize_tweet(tweet):
    return set(nltk.word_tokenize(tweet))


def extract_features(document):
    document_words = tokennize_tweet(document)
    features = {}
    for word in word_features:
        features[word] = (word in document_words)
    return features