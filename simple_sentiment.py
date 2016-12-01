from pymongo import MongoClient
import nltk
import marshal

with open('senti_dict/neg.set','rb') as nf:
    neg = marshal.load(nf)

with open('senti_dict/pos.set','rb') as pf:
    pos = marshal.load(pf)

client = MongoClient('mongodb://syz:password@ec2-52-211-37-84.eu-west-1.compute.amazonaws.com:27017/twitter')
db = client.twitter
#print (db.collection_names())
#'corn_collection', 'sugar_collection', 'coffee_collection', 'milk_collection'
collection = db.coffee_collection
""""
l = []
for i in range(0,100):
    l.append(collection.find_one())


record = collection.find_one()
hashtags = record.get('Hashtages')
tweet = record.get('Text')
"""

pc = 0
nc = 0
#nltk.tokenize(tweet)
# count  collection    pos    neg
#           corn       306    244
#           sugar      953    548
#           coffee    3225    766
#           milk
fs = open("senti_tweet_pos",'a',encoding='UTF-8')
fn = open("senti_tweet_neg",'a',encoding='UTF-8')
for i in collection.find():
    tweet = i.get('Text')
    w_list = nltk.word_tokenize(tweet)
    w_set = set(w_list)
    score = len(pos&w_set) - len(neg&w_set)
    if score>=4:
        fs.write(tweet)
        fs.write('\n')
    elif score<=-4:
        fn.write(tweet)
        fn.write('\n')
fs.close()
fn.close()
