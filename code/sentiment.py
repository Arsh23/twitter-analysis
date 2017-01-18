import json
import requests
import pprint
from collections import Counter

from pymongo import MongoClient
# Using a module i made for async requests -
# https://github.com/Arsh23/asynchronizer
from asynchronizer import asynchronize, Wait, setWorkers

client = MongoClient()
db = client.precog
setWorkers(32)

api_key = 'ADD API KEY HERE'
base_url = 'https://api.havenondemand.com/1/api/sync/analyzesentiment/v2'
usrs = 'DelhiPolice MumbaiPolice KolkataPolice punecitypolice hydcitypolice'
session = requests.session()


@asynchronize
def get_sentiment(text, lst):
        url = ''.join([base_url, '?apikey=', api_key, '&text="', text, '"'])
        d = json.loads(session.get(url).text)
        try:
            lst.append(d['sentiment_analysis'][0]['aggregate']['sentiment'])
            print('done: ', text)
        except Exception:
            print(d)


def get_user_sentiments(user):
    lst = list()
    texts = [x['text'] for x in db[user].find() if len(x['text'].split()) > 1]
    for text in texts:
        get_sentiment(text, lst)
    Wait()
    counter = Counter(lst)
    return [{x: counter[x]} for x in counter.keys()]


def get_sentiments():
    return {user: get_user_sentiments(user) for user in usrs.split()}

data = get_sentiments()
with open('sentiment.json', 'w') as outfile:
    json.dump(data, outfile)
pprint.pprint(data)
