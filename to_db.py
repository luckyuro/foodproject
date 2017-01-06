import pymysql as maria
from utils import classifier, extract_features
import pymongo
from pymongo import MongoClient

connection = maria.connect(host='svm-js1n16-comp6235-temp.ecs.soton.ac.uk',
                           user='test',
                           password='test',
                           db='senti',
                           cursorclass=maria.cursors.DictCursor)
maria_cursor = connection.cursor()

client = MongoClient('mongodb://syz:password@svm-ys3n15-comp6235-temp.ecs.soton.ac.uk:27017/test')
db = client.test
#collection_names = db.collection_names()[1:]
collection_names = ['starbuck_collection', 'sbux_collection', 'costa_coffee_collection', \
                    'kfc_collection', 'costa_collection', 'mcdonalds_collection', 'starbucks_collection']
# format (collection name, collection object)
#collections = [(x, eval('db.'+x)) for x in collection_names]
#print(collection_names)

def foo(records, name):
    collection = name
    c = 0
    for item in records:
        date_str = item.get('Date').strftime('%Y-%m-%d %H:%M:%S')
        retweets= item.get('Retweets') + 1
        object_id = str(item.get('_id'))

        tweet = item.get('Text')
        result = classifier.prob_classify(extract_features(tweet))
        pos = result.prob('positive')
        neg = result.prob('negative')
        bias = classifier.classify(extract_features(tweet))[:3]
        sql = "INSERT INTO `test` (`object_id`,`retweets`,`times`,`collection`,`pos`,`neg`,`bias`) " \
              "VALUES (\"%s\", %d, \"%s\", \"%s\", %lf, %lf, \"%s\") " \
              "ON DUPLICATE KEY UPDATE " \
              "object_id=\"%s\""
#        print(sql%(object_id,retweets,date_str,collection,pos,neg,bias,object_id))
        maria_cursor.execute(sql%(object_id,retweets,date_str,collection,pos,neg,bias,object_id))

        c += 1
        if c > 150 :
            print('commit')
            connection.commit()
            c = 0


#        sql = "INSERT INTO `test` (`object_id`,`retweets`,`times`,`collection`,`pos`,`neg`,`bias`) " \
#              "VALUES (\"%s\", %d, \"%s\", \"%s\", %lf, %lf, %s) "
#        print(sql%(object_id,retweets,date_str,collection,pos,neg,bias))
#        maria_cursor.execute(sql%(object_id,retweets,date_str,collection,pos,neg,bias))

    connection.commit()


for name in collection_names:
    b = eval('db.'+name)
    sql_d = 'SELECT object_id from tweets where collection =\"%s\" ORDER BY object_id DESC LIMIT 10'%name
    maria_cursor.execute(sql_d)
    oid = maria_cursor.fetchone().get('object_id')
    from bson.objectid import ObjectId
    records = b.find({'_id':{'$gt':ObjectId(oid)}},no_cursor_timeout=True)
    foo(records,name)
    records.close()
