# https://www.youtube.com/watch?v=fD-GRCH_tks

from os import environ
from tweepy import Client
from dotenv import load_dotenv
from tenacity import retry, wait_fixed, stop_after_attempt
from requests_html import HTMLSession


def check_hashtag(string):
    return string if "#" in string else f"#{string}"


@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def tweet(client: Client):
    topic = [
        response
        for response in HTMLSession()
        .get("https://news.yahoo.co.jp/flash")
        .html.find("a")
        if "https://news.yahoo.co.jp/articles/" in next(iter(response.links))
    ][0]
    topic_text = topic.attrs["aria-label"]
    topic_url = topic.attrs["href"]

    client.create_tweet(text=f"{topic_text}\n{topic_url}\n\n#最新ニューズピックス")


if __name__ == "__main__":
    load_dotenv()
    tweepy_client = Client(
        consumer_key=environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=environ["TWITTER_CONSUMER_SECRET"],
        access_token=environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    tweet(tweepy_client)
