CREATE TABLE tweets(
object_id CHAR(24),
retweets INT,
times DATETIME,
collection VARCHAR(30),
pos DOUBLE,
neg DOUBLE,
bias CHAR(3),
PRIMARY KEY (object_id)
);

# monthly every day five
#select * from tweets where group by

CREATE TABLE agg(
pos_retweets INT,
neg_retweets INT,
time_point DATETIME,
collection VARCHAR(30),
final_score DOUBLE,
difference INT,
PRIMARY KEY (time_point,collection)
);


CREATE TABLE agg_test(
pos_retweets INT,
neg_retweets INT,
time_point DATETIME,
collection VARCHAR(30),
final_score DOUBLE,
difference INT,
PRIMARY KEY (time_point,collection)
);



CREATE TABLE result(
collection VARCHAR(30),
final_score DOUBLE,
stock_price DOUBLE,
open_price DOUBLE,
time_point DATETIME,
PRIMARY KEY (time_point,collection)
);

CREATE TABLE result_set(
collection VARCHAR(30),
final_score DOUBLE,
stock_price DOUBLE,
open_price DOUBLE,
time_point DATETIME,
PRIMARY KEY (time_point,collection)
);