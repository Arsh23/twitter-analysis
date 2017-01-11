
import re
from lxml import html


def parse_text(tweet):
    text = ''
    for elem in tweet.xpath('.//p[contains(@class, "tweet-text")]/node()'):
        if isinstance(elem, html.HtmlElement):
            if elem.tag == 'a':
                text += ' '+''.join(elem.xpath('.//text()'))+' '
        else:
            text += ' '+elem+' '
    text = ' '.join(text.split())
    text = text.encode('ascii', 'replace')
    return text


def parse_time(tweet):
    t = dict()
    time = tweet.xpath('.//small[@class="time"]/a/@title')[0]
    res = re.findall(r"(\d+):(\d+)\s(\w+)\s-\s(\d+)\s(\w+)\s(\d+)", time)[0]
    t['hour'], t['min'], t['period'], t['day'], t['month'], t['year'] = res
    return t


def parse_tweets(tweets, user):
    parsed_tweets = list()
    for t in tweets:
        tweet = dict()
        tweet['user'] = user
        tweet['text'] = parse_text(t)
        tweet['time'] = parse_time(t)

        rt_xpath = './/button[contains(@class,"js-actionRetweet")]'\
                   '//div[@class="IconTextContainer"]//span/text()'
        tweet['retweets'] = t.xpath(rt_xpath)[1]

        lk_xpath = './/button[contains(@class,"js-actionFavorite")]'\
                   '//div[@class="IconTextContainer"]//span/text()'
        tweet['likes'] = t.xpath(lk_xpath)[1]

        link_xpath = './/ancestor::div[contains(@class,"tweet")]'\
                     '/@data-permalink-path'
        tweet['link'] = t.xpath(link_xpath)[0]

        hashtag_xpath = './/a[contains(@class,"twitter-hashtag")]/b/text()'
        tweet['hashtags'] = ['#'+x.lower() for x in t.xpath(hashtag_xpath)]

        imgs = t.xpath('.//div[contains(@class,"AdaptiveMedia")]')
        tweet['contains_imgs'] = True if imgs else False

        parsed_tweets.append(tweet)
    return parsed_tweets
