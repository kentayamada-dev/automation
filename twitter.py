# https://www.youtube.com/watch?v=fD-GRCH_tks

from os import environ
from random import choice, sample
from tweepy import Client
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from retry import retry
from chrome_driver import get_chrome_driver


def check_hashtag(string: str):
    return string if "#" in string else f"#{string}"


@retry(tries=5, delay=5)
def tweet(client: Client):
    chrome_driver = get_chrome_driver()
    chrome_driver.get("https://twittrend.jp/")
    trend_list = [
        chrome_driver.find_element(By.XPATH, f"//li[{i}]/p/a").text
        for i in range(1, 5)
    ]
    trends = [check_hashtag(trend) for trend in sample(trend_list, choice(range(1, 3)))]
    trends_hashtags = " ".join(trends) + " #最新ニューズピックス"
    chrome_driver.get("https://news.yahoo.co.jp/flash")
    topic = chrome_driver.find_element(
        By.XPATH, "//*[@id='contentsWrap']/div[1]/div[2]/div/a"
    )
    topic_text = topic.find_element(By.TAG_NAME, "p").text
    topic_url = topic.get_attribute("href")

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
