from flask import Flask, url_for,request
import json
import pymysql as maria
from falsk_cors import CORS, cross_origin

app = Flask(__name__)

connection = maria.connect(host='svm-js1n16-comp6235-temp.ecs.soton.ac.uk',
                           user='test',
                           password='test',
                           db='senti',
                           cursorclass=maria.cursors.DictCursor)
maria_cursor = connection.cursor()

def from_db(table,name,start,end):
    sql = """SELECT `final_score` as score ,UNIX_TIMESTAMP(time_point) as date FROM %s WHERE collection ="%s" AND time_point BETWEEN "%s" AND "%s" """%(table,name,start,end)
    maria_cursor.execute(sql)
    return maria_cursor.fetchall()

table_name = {'week':'v_agg_test_week','month':'v_agg_test_month','day':'v_agg_test_day'}

@app.route('/welcome')
def api_root():
    return 'Welcome'
    

@app.route('/all/<collection>')
@cross_origin
def api_all(collection):
    #table = table_name.get(collection)
    start = "2016-10-25 00:00:00"
    end = "2016-12-31 23:59:59"
    return json.dumps(from_db('agg_test',collection,start,end))

#2016-01-03
@app.route('/day/<collection>')
@cross_origin
def api_period(collection):
    #table = table_name.get(collection)
    date =  request.args.get('date',None)
    if date:
        start = date+' 00:00:00'
        end = date+' 23:59:59'
    if date:
        return json.dumps(from_db('agg_test',collection,start,end))
    else:
        return json.dumps({'ERROR':'VALUE MISSED'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=27017)