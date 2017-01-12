import csv
import pymysql as maria
from pymongo import MongoClient

connection = maria.connect(host='svm-js1n16-comp6235-temp.ecs.soton.ac.uk',
                           user='test',
                           password='test',
                           db='senti',
                           cursorclass=maria.cursors.DictCursor)
maria_cursor = connection.cursor()

def data_from_csv(file_name):
    l = []
    with open(file_name,'rt') as f:
        r = csv.reader(f)
        for ele in r:
            l.append((ele[0],ele[1],ele[4]))
    return l


i_sql = "INSERT INTO `result_set` (`time_point`,`stock_price`,`collection`,`open_price`) " \
              "VALUES (FROM_UNIXTIME(%s), %s, \"%s\", %s) " \
              "ON DUPLICATE KEY UPDATE " \
              "collection=\"%s\" AND time_point=FROM_UNIXTIME(%s)"

def insert_price_to_db(filename,collection_name,head=False):
    l = data_from_csv(filename)
    if head:
        l = l[1:]
    for item in l:
        ts = item[0]
        price = item[1]
        open_price = item[2]
        col = collection_name
        sql = i_sql%(ts,price,col,open_price,col,ts)
        maria_cursor.execute(sql)

def calculate_score(cursor):
    result = None
    total_result = 0
    total_retweets = 0
    influence = {'pos':0,'neg':0}
    for record in cursor:
        pos = record.get('pos')
        neg = record.get('neg')
        retweets = record.get('retweets')

        influence[record.get('bias')] += 1
        total_result = total_result+(pos-neg)*retweets
        total_retweets = total_retweets+retweets
    if total_retweets !=0 :
        score = total_result / total_retweets
        difference = int(score/abs(score)) * (influence.get('pos') - influence.get('neg'))
    else:
        score = 0
        difference = 0
    return score


a_sql = "SELECT * FROM tweets " \
    "WHERE tweets.collection = \'%s\' " \
    "AND tweets.times BETWEEN %s AND %s"

u_sql = "UPDATE result_set SET final_score=%lf WHERE collection=\'%s\' AND time_point=%s"

def update_result():
    maria_cursor.execute('select UNIX_TIMESTAMP(time_point) as time ,collection as col from result_set')
    time_col = maria_cursor.fetchall()
    for item in time_col:
        col = item['col']
        time = str(item['time'])
        end = 'FROM_UNIXTIME('+time+')'
        start = 'SUBTIME(FROM_UNIXTIME('+time+'),\'1:0:0\')'
        maria_cursor.execute(a_sql%(col,start,end))
        score = calculate_score(maria_cursor)
        maria_cursor.execute(u_sql%(score,col,end))
        connection.commit()

insert_price_to_db('sbux.csv','sbux_collection',head=True)
insert_price_to_db('mcd.csv','mcd_collection',head=False)
connection.commit()
update_result()