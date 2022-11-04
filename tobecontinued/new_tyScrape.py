### README ###
# Limites de la API:
# https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
##
# Requests / 15-min window (user auth)  180
# Requests / 15-min window (app auth)   450
#

#pip install tweepy
#pip install configparser
#pip install pandas


import configparser
import tweepy
import time

# # read config
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authenticate
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# public_tweets = api.home_timeline()
#print(public_tweets)


timestr = time.strftime("%Y%m%d-%H%M%S")

"""
If you don't understand search queries, there is an excellent introduction to it here: 
https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/5-how-to-write-search-queries.md
"""

# Get tweets that contain the hashtag #petday
# -is:retweet means I don't want retweets
# lang:en is asking for the tweets to be in english

twapi = tweepy.API(auth)

# word "word" (word) -noword (#word) (from:word) (to:word) (@word) min_replies:1 min_faves:1 min_retweets:1 lang:es until:2022-12-01 since:2022-01-01
word_qry = 'messi'
date_since = "2022-01-06" # Year-Day-Month
date_until = "2022-01-10"
min_faves = '0'
query = f"{word_qry} min_faves:{min_faves} until:{date_until} since:{date_since}"
#query = "%s min_faves:%s until:%s since:%s" % (word_qry, min_faves, date_since, date_until)
print(query+timestr)
tweets = twapi.search_tweets(query, count = 5000, tweet_mode = 'extended')


import pandas as pd

# create dataframe
columns = ['Time', 'User', 'Tweet ID', 'Tweet FULL']

data = []

for tweet in tweets:
    try:
        text = tweet.retweeted_status.full_text 
    except AttributeError: 
        text = tweet.full_text
    data.append([tweet.created_at, tweet.user.screen_name, tweet.id, text])

df = pd.DataFrame(data, columns=columns)

import datetime
def _getToday():
        return datetime.date.today().strftime("%Y%m%d")
# outpath = r'C:\test'
filename = "%s-%s.%s" % (word_qry, timestr ,"csv")

df.to_csv(filename)