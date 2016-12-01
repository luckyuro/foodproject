import nltk
import pickle

c = 0

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

def w_freq():
    l = []
    l = tokennize('senti_tweet_neg',l)
    l = tokennize('senti_tweet_pos',l)
    l = nltk.FreqDist(l)

    with open("middle_filr/wordFreq.pickle",'wb') as f:
        pickle.dump(l,f)

#print (l.keys())
print(c)