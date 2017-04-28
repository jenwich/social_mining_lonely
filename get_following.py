import sys
import pymongo
import tweepy
import time
from datetime import datetime
from secret import *

if len(sys.argv) < 3:
    print("Input USER_FROM and USER_TO")
    exit()
else:
    USER_FROM = int(sys.argv[1])
    USER_TO = int(sys.argv[2])
    if (USER_TO < USER_FROM):
        print("USER_TO must greater than USER_FROM")
        exit()

client = pymongo.MongoClient('mongodb://%s:%d/' % (MONGODB_HOST, MONGODB_PORT))
db = client[MONGODB_DATABASE]
db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD)

users = db.user.find().sort('_id', pymongo.ASCENDING).skip(USER_FROM-1).limit(USER_TO-USER_FROM+1)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

test = [users[0]]

def get_user_following(_id):
    friends = tweepy.Cursor(api.friends_ids, user_id=_id, stringify_ids=True).items(5000)
    return list(friends)

for index, u in enumerate(users):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("["+now+"]", end=" ")
    while (True):
        try:
            friends = get_user_following(u['_id'])
        except tweepy.error.RateLimitError:
            print("Rate Limit Error")
            time.sleep(180)
        except tweepy.TweepError:
            print("Tweepy Error")
            time.sleep(180)
        else:
            break
    db.user.update({'_id': u['_id']}, {'friends': friends}, upsert=True)
    print("User#%d (%s): %d friends have added to database" % (USER_FROM+index, u['screen_name'], len(friends)))
    time.sleep(60)
