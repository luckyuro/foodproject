import nltk
import pickle
from langdetect import detect
from nltk.corpus import words, stopwords
c = 0
with open("middle_file/wordFreq.pickle","rb") as f:
    word_features = pickle.load(f)
stop = set(stopwords.words('english'))
en_words = words.words()

def tokennize(filename, theobj):
    with open(filename,'r',encoding='UTF-8') as f:
        while True:
            try:
                line = f.readline()
                if not line: break
                if detect(line) != 'en':
                    continue
            except:
                continue
            tweet_words = nltk.word_tokenize(line)
            global c
            c +=1
            for word in tweet_words:
                if (word in en_words) and (word not in stop):
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
        features[word] = (word in document_words)
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
            if not tweet: break
            features = extract_features(tweet)
            result.append((features,value))
        except UnicodeError:
            continue
    return result


""""
def generate_tuple(filename, value):
    ls = []
    with open(filename) as f:
        while True:
            try:
                tweet = f.readline()
                if not tweet: break
                ls.append((tweet,value))
            except UnicodeError:
                continue
    return ls
"""


def train_set_file():
    # l = generate_tuple("senti_tweet_neg",'positive')
    with open("senti_tweet_neg",'r') as fn, open("senti_tweet_pos",'r') as fp,\
            open("middle_file/train_set.pickle","wb") as ts:
        l = build_train_set(fp,'positive')
        l.extend(build_train_set(fn,'negative'))
        import random
        random.shuffle(l)
        print (len(l))
        pickle.dump(l, ts)


def navieBtrain():
    with open("middle_file/train_set.pickle","rb") as ts:
        train_set = pickle.load(ts)
        print('start training')
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        print('training finished')
        print(classifier.show_most_informative_features(32))
        with open("middle_file/classifier.pickle","wb") as cl:
            pickle.dump(classifier,cl)

#nltk.classify.apply_features
with open("middle_file/classifier.pickle","rb") as cl:
    classifier = pickle.load(cl)

s = "Candy corn trash they need to stop making that bullshit I wouldn't give my worst enemy candy corn , it taste like broken dreams and death https:// twitter.com/liveforxo_/sta tus/788649123029262337"
print(classifier.classify(extract_features(s)))


#prepare frequency
#w_freq()
#print(c)
#train set
#train_set_file()
#train
#navieBtrain()
