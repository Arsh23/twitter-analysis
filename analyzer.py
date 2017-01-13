
import pprint
from collections import Counter
from datetime import datetime as dt

from pymongo import MongoClient

client = MongoClient()
db = client.precog


usrs = 'DelhiPolice MumbaiPolice KolkataPolice punecitypolice hydcitypolice'


def calc_top10(user):
    tweets = db[user].find({'hashtags': {'$gt': []}})
    counter = Counter(tag for tweet in tweets for tag in tweet['hashtags'])
    return {x: y for x, y in counter.most_common(10)}


def get_top10(users):
    return {user: calc_top10(user) for user in users.split()}


def calc_freq(u):
    d = (dt.strptime(x['time'], '%I:%M %p - %d %b %Y') for x in db[u].find())
    counter = Counter('{}-{}'.format(x.weekday(), x.hour) for x in d)
    return {x: counter[x] for x in counter.keys()}


def get_freq(users):
    return {user: calc_freq(user) for user in users.split()}


pprint.pprint(get_top10(usrs))
pprint.pprint(get_freq(usrs))
