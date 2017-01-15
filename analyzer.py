
import re
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
    return [{'tag': x, 'amt': counter[x]} for x in counter.keys()]


def get_top10(users):
    return {user: calc_top10(user) for user in users.split()}


def get_dict(x, counter):
    return {'day': x.split('-')[0], 'hr': x.split('-')[1], 'amt': counter[x]}


def calc_freq(u):
    d = (dt.strptime(x['time'], '%I:%M %p - %d %b %Y') for x in db[u].find())
    counter = Counter('{}-{}'.format(x.weekday(), x.hour) for x in d)
    return [get_dict(x, counter) for x in counter.keys()]


def get_freq(users):
    return {user: calc_freq(user) for user in users.split()}


'''
for user in usrs.split():
    tweets = db[user].find({'contains_imgs':True})
    for tweet in tweets:
        text = re.sub(r"pic.twitter.com\/[\w\d]+(?:\s|$)", '', tweet['text'])
        if len(text.split()) <=3:
            # print user,text, tweet['contains_imgs']
            pass

def calc_egmt(user):
    i = db[user].find({'contains_imgs':True})
    # regex =
    t = (re.sub(r"pic.twitter.com\/[\w\d]+(?:\s|$)", '', x['text']) for x in i)
    print len(t)

for user in usrs.split():
    calc_egmt(user)
'''
pprint.pprint(get_top10(usrs))
pprint.pprint(get_freq(usrs))
