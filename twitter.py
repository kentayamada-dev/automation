# https://www.youtube.com/watch?v=fD-GRCH_tks

from os import environ
from datetime import datetime, timedelta, timezone
from random import choice
from tweepy import Client
from dotenv import load_dotenv
from tenacity import retry, wait_fixed, stop_after_attempt
from requests_html import HTMLSession

IS_EVEN_MIN = datetime.now(timezone(timedelta(hours=+9), "JST")).minute % 2 == 0


def check_hashtag(string):
    return string if "#" in string else f"#{string}"


@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def tweet(client: Client):
    data = HTMLSession().get("https://news.yahoo.co.jp/flash").html.find("a")
    topic = (
        [
            response
            for response in data
            if "https://news.yahoo.co.jp/articles/" in next(iter(response.links))
        ][0]
        if IS_EVEN_MIN
        else choice(
            [
                response
                for response in data
                if "https://news.yahoo.co.jp/pickup/" in next(iter(response.links))
            ]
        )
    )
    topic_text = topic.attrs["aria-label"] if IS_EVEN_MIN else topic.text
    topic_url = topic.attrs["href"]

    client.create_tweet(text=f"{topic_text}\n\n#最新ニューズピックス\n{topic_url}")


if __name__ == "__main__":
    load_dotenv()
    tweepy_client = Client(
        consumer_key=environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=environ["TWITTER_CONSUMER_SECRET"],
        access_token=environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    tweet(tweepy_client)
