
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


def parse_tweets(tweets):
    for t in tweets:
        tweet = dict()
        tweet['text'] = parse_text(t)
        print tweet
        # time = t.xpath('.//small[@class="time"]/a/@title')
        # tweet['time'] = apply regex
