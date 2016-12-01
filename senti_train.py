import nltk
import pickle

c = 0
with open("middle_file/wordFreq.pickle","rb") as f:
    word_features = pickle.load(f)


def tokennize(filename, theobj):
    with open(filename,'r',encoding='UTF-8') as f:
        while True:
            try:
                line = f.readline()
            except:
                continue
            if not line: break
            tweet_words = nltk.word_tokenize(line)
            #global c
            #c +=1
            for word in tweet_words:
                if len(word)>3:
                    if isinstance(theobj,list):
                        theobj.append(word)
                    elif isinstance(theobj,set):
                        theobj.add(word)
                    else:
                        pass
    return theobj


def tokennize_tweet(tweet):
    return set(nltk.word_tokenize(tweet))


def w_freq():
    l = []
    l = tokennize('senti_tweet_neg',l)
    l = tokennize('senti_tweet_pos',l)
    l = nltk.FreqDist(l)

    with open("middle_file/wordFreq.pickle",'wb') as f:
        pickle.dump(l,f)


def extract_features(document):
    document_words = tokennize_tweet(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

#print (l.keys())
#print(c)
#with open("middle_file/wordFreq.pickle","rb") as f:
#    l = pickle.load(f)
#print ('instart' in l)


def build_train_set(f, value):
    result = []
    while True:
        try:
            tweet = f.readline()
            features = extract_features(tweet)
            result.append((features,value))
        except UnicodeError:
            continue
    return result

with open("senti_tweet_neg") as f:
    r = build_train_set(f, 'negative')

print (r)