import got

def main():

	def printTweet(descr, t):
		# print descr
		pass
		#print "Username: %s" % t.username
		# print "Retweets: %d" % t.retweets
		# print "Text: %s" % t.text.encode("utf-8")
		# print "Mentions: %s" % t.mentions
		# print "Hashtags: %s\n" % t.hashtags

	# Example 1 - Get tweets by username
	#tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
	#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	#tweet.Text
    #tweet.text.encode('utf-8')
	#printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

	# Example 2 - Get tweets by query search
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('costa').setSince("2016-10-01").setUntil("2016-11-01").setMaxTweets(100000000)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)
	#tweet["Text"]
    #tweet.text.encode('utf-8')
	#printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)

	# Example 3 - Get tweets by username and bound dates
	#tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2012-09-11").setUntil("2016-09-12").setMaxTweets(1000)
	#for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
	#print (type(tweet))
    #tweet.Text
    #tweet.text.encode('utf-8')
	 #  printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)

if __name__ == '__main__':
	main()

