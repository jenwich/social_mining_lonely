import sys
import pymongo
from datetime import datetime
from secret import *

if len(sys.argv) < 3:
    print("Input FROM and TO")
    exit()
else:
    FROM = int(sys.argv[1])
    TO = int(sys.argv[2])
    if (TO < FROM):
        print("TO must greater than FROM")
        exit()

SIZE_LIMIT = 10000

client = pymongo.MongoClient('mongodb://%s:%d/' % (MONGODB_HOST, MONGODB_PORT))
db = client[MONGODB_DATABASE]
db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD)

users_ = db.user.find({'friends': {'$exists': True}, 'screen_name': {'$exists': True}}, no_cursor_timeout=True).limit(SIZE_LIMIT).sort('_id', pymongo.ASCENDING)
print("Total:", users_.count(), "users, Size limit:", SIZE_LIMIT)
print("Loading data...")
users = list(users_)
users_.close()

if FROM < 0:
    print("FROM must not be negative")
    exit(1)
if TO >= len(users):
    print("TO is too much (number of user is %d, max of TO is %d)" % (len(users), len(users)-1))
    exit(1)

def now():
    now_ = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return "["+ now_ +"]"

for i_, u in enumerate(users[FROM: TO+1]):
    i = i_ + FROM

    if bool(db.friend_coeff.find_one({'_id': i})):
        print(now(), "Duplicate key %d, skipped." % i)
        continue

    coeff = []
    for v in users:
        if u == v:
            coeff.append(-1)
        else:
            intersect_count = len(set(u['friends']).intersection(set(v['friends'])))
            union_count = len(set(u['friends']).union(set(v['friends'])))
            if (union_count == 0):
                coeff.append(0)
            else:
                coeff.append(intersect_count/union_count)
    obj = {
        '_id': i,
        'user_id': u['_id'],
        'screen_name': u['screen_name'],
        'friend_coeff': coeff
    }
    try:
        db.friend_coeff.insert(obj)
    except pymongo.errors.DuplicateKeyError:
        print(now(), "Duplicate key %d, skipped." % i)
        continue
    except Exception as e:
        print(e)
        raise
    else:
        print(now(), "Calculate friend_coeff for User#%d" % i)
