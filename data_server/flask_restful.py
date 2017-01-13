from flask import Flask, url_for,request
import json
import pymysql as maria
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import AutoReconnect
import time
from bson import json_util




app = Flask(__name__)

connection = maria.connect(host='svm-js1n16-comp6235-temp.ecs.soton.ac.uk',
                           user='test',
                           password='test',
                           db='senti',
                           cursorclass=maria.cursors.DictCursor)
maria_cursor = connection.cursor()

client = MongoClient('mongodb://syz:password@svm-ys3n15-comp6235-temp.ecs.soton.ac.uk:27017/test')
db = client.test

def check_maria_connection():
    if connection.open:
        pass
    else:
        connection.connect()

def mongo_by_id(col,id_str):
    try:
        return col.find_one({"_id": ObjectId(id_str)},{"_id":0})
    except AutoReconnect:
        time.sleep(2)
        return col.find_one({"_id": ObjectId(id_str)},{"_id":0})

def from_db(table,name,start,end):
    check_maria_connection()
    sql = """SELECT `final_score` as price ,UNIX_TIMESTAMP(time_point) as date FROM %s WHERE collection ="%s" AND time_point BETWEEN "%s" AND "%s" """%(table,name,start,end)
    maria_cursor.execute(sql)
    return maria_cursor.fetchall()

def result(collection):
    check_maria_connection()
    sql = """SELECT UNIX_TIMESTAMP(time_point) AS date, `stock_price` AS price, `final_score` AS score FROM result WHERE collection='%s' """
    maria_cursor.execute(sql%collection)
    return maria_cursor.fetchall()

def result_set(collection):
    check_maria_connection()
    sql = """SELECT UNIX_TIMESTAMP(time_point) AS date, `stock_price` AS price, `final_score` AS score, `open_price` AS open FROM result_set WHERE collection='%s' """
    maria_cursor.execute(sql%collection)
    return maria_cursor.fetchall()

def get_tweets(collection, timestamp):
    check_maria_connection()
    sql = "SELECT object_id FROM tweets WHERE collection = \'%s\'and times between SUBTIME(FROM_UNIXTIME(%s),\'1:0:0\') and FROM_UNIXTIME(%s) ORDER BY retweets DESC LIMIT 25"%(collection,timestamp,timestamp)
    maria_cursor.execute(sql)
    idl = [x['object_id'] for x in maria_cursor]
    col = eval('db.'+collection)
    return [mongo_by_id(col,x) for x in idl]




table_name = {'week':'v_agg_test_week','month':'v_agg_test_month','day':'v_agg_test_day'}

@app.route('/welcome')
def api_root():
    return 'Welcome'


@app.route('/all/<collection>')
@cross_origin()
def api_all(collection):
    #table = table_name.get(collection)
    start = "2016-10-25 00:00:00"
    end = "2016-12-31 23:59:59"
    return json.dumps(from_db('agg_test',collection,start,end))

#2016-01-03
@app.route('/day/<collection>')
@cross_origin()
def api_day(collection):
    #table = table_name.get(collection)
    date =  request.args.get('date',None)
    if date:
        start = date+' 00:00:00'
        end = date+' 23:59:59'
    if date:
        return json.dumps(from_db('agg_test',collection,start,end))
    else:
        return json.dumps({'ERROR':'VALUE MISSED'})

@app.route('/old_result/<collection>')
@cross_origin()
def api_period(collection):
    return json.dumps(result(collection))

@app.route('/result/<collection>')
@cross_origin()
def api_period_new(collection):
    return json.dumps(result_set(collection))

@app.route('/tweets/<collection>/<timestamp>')
def api_get_tweets(collection,timestamp):
    return json.dumps(get_tweets(collection,str(timestamp)),default=json_util.default)




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=27017)