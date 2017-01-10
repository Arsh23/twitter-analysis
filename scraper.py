
import time
from lxml import html

from selenium import webdriver
from parser import parse_tweets

url = 'https://twitter.com/DelhiPolice'


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
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(3)

    for tweet in get_tweet_objs(driver):
        if len(tweet.xpath('.//div[@class="context"]//text()')) == 1:
            tweets.append(tweet.xpath('.//div[@class="content"]'))
        if len(tweets) == num:
            print('Extracted {} tweets'.format(num))
            break

    tweets = [x[0] for x in tweets]
    return parse_tweets(tweets)


if __name__ == '__main__':
    user = 'DelhiPolice'
    driver = webdriver.Firefox()
    print(extract_tweets(driver,  user, 5))
    driver.close()
