import json
from pymongo import MongoClient
import time
from datetime import datetime
from dateutil import tz
from secret import *

import numpy as np

client = MongoClient('mongodb://%s:%d/' % (MONGODB_HOST, MONGODB_PORT))
db = client[MONGODB_DATABASE]
db.authenticate(MONGODB_USERNAME, MONGODB_PASSWORD)

tweets = db.tweet.find()
users = [t['user']['screen_name'] for t in tweets]

users = np.array(users)
unique, count = np.unique(users, return_counts=True)
freq = np.asarray((unique, count)).T
freq = [tuple(i) for i in freq]

freq = sorted(freq, key=lambda x: (int(x[1]), x[0]), reverse=True)

with open('users.txt', 'w+') as file:
    file.write('\n'.join(list([str(i[1])+"\t"+str(i[0]) for i in freq])))

