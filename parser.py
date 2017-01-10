
import re
from lxml import html


def parse_text(tweet):
    text = list()
    for elem in tweet.xpath('.//p[contains(@class, "tweet-text")]/node()'):
        if isinstance(elem, html.HtmlElement):
            if elem.tag == 'a':
                text += [' ', ''.join(elem.xpath('.//text()')), ' ']
        else:
            text += [' ', elem, ' ']
    text = ''.join(text)
    text = ' '.join(text.split())
    text = text.encode('ascii', 'replace')
    return text


def parse_time(tweet):
    t = dict()
    time = tweet.xpath('.//small[@class="time"]/a/@title')[0]
    res = re.findall(r"(\d+):(\d+)\s(\w+)\s-\s(\d+)\s(\w+)\s(\d+)", time)[0]
    t['hour'], t['min'], t['period'], t['day'], t['month'], t['year'] = res
    return t


def parse_tweets(tweets):
    for t in tweets:
        tweet = dict()
        tweet['text'] = parse_text(t)
        tweet['time'] = parse_time(t)
        # tweet['time'] = apply regex
