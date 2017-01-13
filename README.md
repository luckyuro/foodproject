# How to use the classifier
## the preparations should be done before using it
This part mainly follows the step in Laurent Luce's Blog
[http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/](http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/)
And also used some achievements from git hub user
[Jeffrey Breen](https://github.com/jeffreybreen) with his repo [jeffreybreen/twitter-sentiment-analysis-tutorial-201107](https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107)
and 
[Richard Everett](https://github.com/RichEverett) with his repo [RichEverett/twitter](https://github.com/RichEverett/twitter)
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

**************

# Use result from Maria(MySQL)
## connecting to mysql database
```python
import pymysql as maria
connection = maria.connect(host='svm-js1n16-comp6235-temp.ecs.soton.ac.uk',
                           user='test',
                           password='test',
                           db='senti',
                           cursorclass=maria.cursors.DictCursor)
```
after connected to the database, the data could be fetch from table agg_test by time_point and collection
for example:
```sql
SELECT * FROM AGG_TEST WHERE time_point='2016-12-02 09:05' and collection='mcd_collection'
```
the tables has the structure
```
pos_retweets INT,
neg_retweets INT,
time_point DATETIME,
collection VARCHAR(30),
final_score DOUBLE,
difference INT,
PRIMARY KEY (time_point,collection)
```

# Restful api
provided apis for data
the main apis are:
```
/result/<collection>
/tweets/<collection>/<timestamp>
```