
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


def get_other_data(user, key, has_img):
    tweets = db[user].find({'contains_imgs': True if has_img else False})
    strs = (x[key].split()[0] for x in tweets if x[key].split() != [])
    return sum(int(x) if x[-1:] != 'K' else float(x[:-1])*1000 for x in strs)


def get_img_only(user, key):
    tweets = db[user].find({'contains_imgs': True})
    regex = r"pic.twitter.com\/[\w\d]+(?:\s|$)"
    t = (x for x in tweets if len(re.sub(regex, '', x['text']).split()) < 4)
    strs = (x[key].split()[0] for x in t if x[key].split() != [])
    return sum(int(x) if x[-1:] != 'K' else float(x[:-1])*1000 for x in strs)


def get_user_eng(user):
    data = list()
    data.append({'text_rt': get_other_data(user, 'retweets', False)})
    data.append({'text_lk': get_other_data(user, 'likes', False)})
    data.append({'both_rt': get_other_data(user, 'retweets', True)})
    data.append({'both_lk': get_other_data(user, 'likes', True)})
    data.append({'imgs_rt': get_img_only(user, 'retweets')})
    data.append({'imgs_lk': get_img_only(user, 'likes')})
    return data


def get_engagement(users):
    return {user: get_user_eng(user) for user in users.split()}


# pprint.pprint(get_top10(usrs))
# pprint.pprint(get_freq(usrs))
pprint.pprint(get_engagement(usrs))
