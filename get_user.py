import pymongo
from secret import *

print("Do not run this file !!!!")
exit(1)

client = pymongo.MongoClient('mongodb://%s:%d/' % (MONGODB_HOST, MONGODB_PORT))
db = client[MONGODB_DATABASE]
db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD)

users= db.tweet.find({}, {'user': 1, 'created_at': 1}).sort('created_at', pymongo.ASCENDING)
users = [i['user'] for i in list(users)]

exit(1)
for u in users:
    db.user.update({'_id': u['_id']}, u, upsert=True)
