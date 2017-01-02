import urllib,urllib2,json,re,datetime,sys,cookielib
from .. import models
from pyquery import PyQuery


class TweetManager:

	def __init__(self):
		pass

	@staticmethod
	def getTweets(tweetCriteria, receiveBuffer = None, bufferLength = 100):
		refreshCursor = ''

		results = []
		resultsAux = []
		cookieJar = cookielib.CookieJar()

		if hasattr(tweetCriteria, 'username') and (tweetCriteria.username.startswith("\'") or tweetCriteria.username.startswith("\"")) and (tweetCriteria.username.endswith("\'") or tweetCriteria.username.endswith("\"")):
			tweetCriteria.username = tweetCriteria.username[1:-1]
		count = 0
		active = True
		file_name = "corn1.json"
		import datetime
		# from langdetect import detect
		from pymongo import MongoClient
		# client = MongoClient('mongodb://localhost:27017')
		client = MongoClient('mongodb://syz:password@svm-ys3n15-comp6235-temp.ecs.soton.ac.uk:27017/test')
		db = client.test
		collection = db.costa_collection
		while active:
			count = count + 1
			json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar)
            #print json
			if len(json['items_html'].strip()) == 0:
				break
            #print json
			refreshCursor = json['min_position']
			tweets = PyQuery(json['items_html'])('div.js-stream-tweet')

			if len(tweets) == 0:
				break
            #print json
			for tweetHTML in tweets:
				tweetPQ = PyQuery(tweetHTML)
				# print tweetHTML
				print "html**************************"
				# print tweetPQ
				tweet = models.Tweet()
				# print type(tweet)
                #print json
				usernameTweet = tweetPQ("span.username.js-action-profile-name b").text();
				txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'));
				lan = tweetPQ("p.js-tweet-text").attr('lang')
				# if it is not english, no need to continue
				if lan != 'en':
					continue
				retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				
				favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
				dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"));
				# print txt
				print dateSec
				id = tweetPQ.attr("data-tweet-id");
				permalink = tweetPQ.attr("data-permalink-path");

				geo = ''
				geoSpan = tweetPQ('span.Tweet-geo')
				if len(geoSpan) > 0:
					geo = geoSpan.attr('title')

				tweet.id = id
				tweet.permalink = 'https://twitter.com' + permalink
				tweet.username = usernameTweet
				tweet.text = txt
				tweet.date = datetime.datetime.fromtimestamp(dateSec)
				tweet.retweets = retweets
				tweet.favorites = favorites
				tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
				tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
				tweet.geo = geo

				#results.append(tweet)
				#resultsAux.append(tweet)
          #       print "Username: %s" % t.username
          #       print "Retweets: %d" % t.retweets
		        # print "Text: %s" % t.text.encode("utf-8")
		        # print "Mentions: %s" % t.mentions
		        # print "Hashtags: %s\n" % t.hashtags
				# print type(tweet.date)
				# print type(tweet.text)
				print (tweet.text.encode("utf-8"))
				print (tweet.date)
				#print tweet.text.encode("utf-8").decode("utf-8")
				# print detect(tweet.text)
				# data_coffee = {"Username": tweet.username, "Retweets": tweet.retweets, "Text": tweet.text.encode("utf-8"), "Mentions": tweet.mentions, "Hashtages": tweet.hashtags, "Date": tweet.date.__str__()}
				data_coffee = {"Id": tweet.id, "Geo": tweet.geo, "Permalink": tweet.permalink, "Favorites": tweet.favorites,"Username": tweet.username, "Retweets": tweet.retweets, "Text": tweet.text.encode("utf-8"), "Mentions": tweet.mentions, "Hashtages": tweet.hashtags, "Date": tweet.date}
				#write to MongoDB
				
				# import json
				# with open(file_name, 'a') as outfile:
				# 	json.dump(data_coffee, outfile)

				collection.insert_one(data_coffee)

				if tweetCriteria.maxTweets > 0 and count >= tweetCriteria.maxTweets:
					active = False
					break


		if receiveBuffer and len(resultsAux) > 0:
			receiveBuffer(resultsAux)

		return results

	@staticmethod
	def getJsonReponse(tweetCriteria, refreshCursor, cookieJar):
		url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

		urlGetData = ''
		if hasattr(tweetCriteria, 'username'):
			urlGetData += ' from:' + tweetCriteria.username

		if hasattr(tweetCriteria, 'since'):
			urlGetData += ' since:' + tweetCriteria.since
			# print tweetCriteria.since
		if hasattr(tweetCriteria, 'until'):
			urlGetData += ' until:' + tweetCriteria.until
			# print tweetCriteria.until
		if hasattr(tweetCriteria, 'querySearch'):
			urlGetData += ' ' + tweetCriteria.querySearch

		if hasattr(tweetCriteria, 'topTweets'):
			if tweetCriteria.topTweets:
				url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"

		url = url % (urllib.quote(urlGetData), refreshCursor)

		headers = [
			('Host', "twitter.com"),
			('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
			('Accept', "application/json, text/javascript, */*; q=0.01"),
			('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
			('X-Requested-With', "XMLHttpRequest"),
			('Referer', url),
			('Connection', "keep-alive")
		]

		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		opener.addheaders = headers

		try:
			response = opener.open(url)
			print (url)
			jsonResponse = response.read()
		except:
			print ("Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData))
			sys.exit()
			return

		dataJson = json.loads(jsonResponse)

		return dataJson
