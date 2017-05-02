import pymongo
from secret import *

client = pymongo.MongoClient('mongodb://%s:%d/' % (MONGODB_HOST, MONGODB_PORT))
db = client[MONGODB_DATABASE]
db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD)

#users_ = db.friend_coeff.find({'friends': {'$exists': True}, 'screen_name': {'$exists': True}}, no_cursor_timeout=True).limit(SIZE_LIMIT).sort('_id', pymongo.ASCENDING)
#users = list(users_)
#users_.close()

users_tweet_ = db.tweet.aggregate([
  {
    '$group': {
      '_id': '$user._id',
      'count': {
        '$sum': 1
      },
      'screen_name': {
        '$last': '$user.screen_name'
      },
      'name': {
        '$last': '$user.name'
      }
    }
  }, {
    '$sort': {
      'count': -1
    }
  }
])

users_tweet_count = {}
users_name = {}
for u in list(users_tweet_):
    users_tweet_count[u['_id']] = u['count']
    users_name[u['_id']] = u['name']
users_tweet_.close()

users_ = db.friend_coeff.find({}, {'friend_coeff': 0})
users = list(users_)
users_.close()

users = sorted(users, key=lambda i: i['_id'])

for u in users:
    u['count'] = users_tweet_count[u['user_id']]
    u['name'] = users_name[u['user_id']]

count_list = [u['count'] for u in users]
name_list = [u['name'] for u in users]

with open('count.txt', 'w+') as f:
    f.write(','.join([str(i) for i in count_list]))

with open('name.txt', 'w+') as f:
    f.write('\n'.join(name_list))

