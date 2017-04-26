import json
import tweepy
from pymongo import MongoClient
import time
from datetime import datetime
from dateutil import tz
from secret import *

client = MongoClient('mongodb://%s:%d/' % (MONGODB_HOST, MONGODB_PORT))
db = client[MONGODB_DATABASE]
db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

with open('keywords.txt') as file:
    keywords = file.read().split('\n')[:-1]

def to_datetime(time_str):
    return datetime.fromtimestamp(time.mktime(time.strptime(time_str,'%a %b %d %H:%M:%S +0000 %Y')))

def as_timezone(dt):
    return dt.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.tzlocal())

def get_tweet_data():
    query_str = ' OR '.join(keywords)
    tweets = tweepy.Cursor(api.search, q=query_str).items(100)
    tweet_dict = [i._json for i in tweets]

    data = [{
            '_id': i['id_str'],
            'text': i['text'],
            'created_at': to_datetime(i['created_at']),
            'user': {
                '_id': i['user']['id_str'],
                'name': i['user']['name'],
                'screen_name': i['user']['screen_name']
            }
        } for i in tweet_dict]
    return data

while (True):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("["+now+"]", end=" ")
    try:
        data = get_tweet_data()
    except tweepy.RateLimitError:
        print("Rate limit exceed.")
        time.sleep(60)
    except tweepy.TweepError:
        raise
    else:
        try:
            tweet_ids = db.tweet.insert_many(data).inserted_ids
        except Exception:
            print("Insert tweets successfully. Some tweets are duplicate.")
        else:
            print("Insert all 100 tweets successfully")
        time.sleep(60)
