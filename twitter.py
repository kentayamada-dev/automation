# https://www.youtube.com/watch?v=fD-GRCH_tks

from os import environ
from datetime import datetime, timedelta, timezone
from random import choice, sample
from tweepy import Client
from dotenv import load_dotenv
from tenacity import retry, wait_fixed, stop_after_attempt
from requests_html import HTMLSession

CURRNET_HOUR_JST = datetime.now(timezone(timedelta(hours=+9), "JST")).hour


def check_hashtag(string):
    return string if "#" in string else f"#{string}"


@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def tweet(client: Client):
    get = HTMLSession().get
    trend_list = (
        get("https://twittrend.jp/")
        .html.find("div#now", first=True)
        .find("p.trend > a")[:5]
    )
    counts = choice(range(1, 2)) if CURRNET_HOUR_JST % 2 == 0 else choice(range(4, 6))
    trends = [
        check_hashtag(trend)
        for trend in sample([trend.text for trend in trend_list], counts)
    ]
    trends_hashtags = " ".join(trends) + " #最新ニューズピックス"
    topic = [
        i
        for i in get("https://news.yahoo.co.jp/flash").html.find("a")
        if "https://news.yahoo.co.jp/articles/" in next(iter(i.links))
    ][0]
    topic_text = topic.attrs["aria-label"]
    topic_url = topic.attrs["href"]

    client.create_tweet(text=f"{topic_text}\n{topic_url}\n\n{trends_hashtags}")


if __name__ == "__main__":
    load_dotenv()
    tweepy_client = Client(
        consumer_key=environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=environ["TWITTER_CONSUMER_SECRET"],
        access_token=environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    tweet(tweepy_client)
