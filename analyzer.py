
import pprint
from collections import Counter

from pymongo import MongoClient

client = MongoClient()
db = client.precog


usrs = 'DelhiPolice MumbaiPolice KolkataPolice punecitypolice hydcitypolice'


def calc_top10(user):
    counter = Counter()
    tweets = db[user].find({'hashtags': {'$gt': []}})
    counter.update(tag for tweet in tweets for tag in tweet['hashtags'])
    return {x: y for x, y in counter.most_common(10)}


def get_top10(users):
    return {user: calc_top10(user) for user in users.split()}


pprint.pprint(get_top10(usrs))
