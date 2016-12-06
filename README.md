# How to use the classifier
## the preparations should be done before using it
* the lib needed
```python
import nltk
import pickle
```
* prepare for the classifier
```python
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
```
# use the classifier
```python
s = """Candy corn trash they need to stop making that bullshit I wouldn't give my worst enemy candy corn , it taste like broken dreams and death https:// twitter.com/liveforxo_/sta tus/788649123029262337 …"""
result = classifier.prob_classify(extract_features(s))
#<class 'nltk.probability.DictionaryProbDist'>, {'_prob_dict': {'positive': -32.30537884272147, 'negative': -2.7182522899238393e-10}, '_log': True}
print (result.prob('positive'))
#1.884134695800929e-10
print (result.prob('negative'))
#0.9999999998115852
print(classifier.classify(extract_features(s)))
#negative
```
