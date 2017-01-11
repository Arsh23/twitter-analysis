
import time
from lxml import html

from selenium import webdriver
from parser import parse_tweets
from pymongo import MongoClient


client = MongoClient()
db = client.precog


def get_tweet_objs(driver):
    tree = html.fromstring(driver.page_source)
    return tree.xpath('//li[@data-item-type="tweet"]')


def extract_tweets(driver, user, num):
    url = 'https://twitter.com/'+user
    driver.get(url)

    print('Starting scraping...')
    tweets = list()
    while True:
        tweets_count = 0
        for tweet in get_tweet_objs(driver):
            if len(tweet.xpath('.//div[@class="context"]//text()')) == 1:
                tweets_count += 1
        if tweets_count >= num:
            print('Loaded {} tweets for user : {}'.format(tweets_count, user))
            break
        print('Got {} tweets'.format(tweets_count))
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(3)

    for tweet in get_tweet_objs(driver):
        if len(tweet.xpath('.//div[@class="context"]//text()')) == 1:
            tweets.append(tweet.xpath('.//div[@class="content"]'))
        # if len(tweets) == num:
            # print('Extracted {} tweets'.format(num))
            # break

    tweets = [x[0] for x in tweets]
    return parse_tweets(tweets, user)


def write_to_db(data, user):
    print('writing to db for {}'.format(user))
    collection = db[user]
    collection.insert_many(data)

if __name__ == '__main__':
    users = 'DelhiPolice MumbaiPolice KolkataPolice BlrCityPolice hydcitypolice'
    driver = webdriver.Firefox()

    for user in users.split():
        print('Extracting from {}'.format(user))
        data = extract_tweets(driver, user, 300)
        write_to_db(data, user)
        print('Extracted from {}'.format(user))
    driver.close()
