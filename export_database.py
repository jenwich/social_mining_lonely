import json
import sys
import pymongo
from secret import *

client = pymongo.MongoClient('mongodb://%s:%d/' % (MONGODB_HOST, MONGODB_PORT))
db = client[MONGODB_DATABASE]
db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD)

if len(sys.argv) < 2:
    print("Input COLLECTION")
    exit(1)
else:
    collection = sys.argv[1]

if collection == 'tweet':
    docs = list(db.tweet.find())
    for d in docs:
        d['created_at'] = d['created_at'].isoformat()
elif collection == 'user':
    docs = list(db.user.find({'friends': {'$exists': 1}, 'screen_name': {'$exists': 1}}))
elif collection == 'friend_coeff':
    docs = list(db.friend_coeff.find())
else:
    print("Invalid collection name")


with open(collection+'.export.json', 'w+') as f:
    data = {}
    data[collection+'s'] = docs
    f.write(json.dumps(data, ensure_ascii=False))
