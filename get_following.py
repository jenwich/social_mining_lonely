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
    now_str = "["+now+"]"
    skip = 0
    while (True):
        try:
            friends = get_user_following(u['_id'])
        except tweepy.error.RateLimitError:
            print(now_str, "Rate Limit Error")
            time.sleep(180)
        except tweepy.TweepError as e:
            print(now_str, "Tweepy Error")
            print(e)
            if str(e) == "Not authorized.":
                skip = 1
                print("Skipped.")
                break
            time.sleep(180)
        else:
            break
    if skip == 1:
        continue
    u_ = u.copy()
    u_['friends'] = friends
    db.user.update({'_id': u['_id']}, u_, upsert=True)
    print(now_str, "User#%d (%s): %d friends have added to database" % (USER_FROM+index, u['screen_name'], len(friends)))
    time.sleep(60)
