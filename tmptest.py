#a = {'2'}
#a.add('1')
#print(type(a))
#a = "thi is  ais a djdiso"
#import nltk
#l = nltk.word_tokenize(a)
#print(l)


from langdetect import detect


def all_en(filename):
    nfilename = filename+'.new'
    with open(filename,'r') as fr, open(nfilename,'w') as fw:
        fr.seek(10)
        while True:
            try:
                print(fr.tell())
                line = fr.readline()
                print (line)
                if not line:
                    break
                if detect(line) != 'en':
                    print (detect(line))
                    continue
                fw.write(line)
            except UnicodeError:
                print("unicode")
                continue

all_en("senti_tweet_neg")