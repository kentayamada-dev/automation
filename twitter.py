import os
import random
import tweepy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from retry import retry


def check_hashtag(string):
    return string if "#" in string else f"#{string}"


def remove_hashtag(string):
    return string.replace("#", "")


def like_follow_by_query(client, query, count):
    tweets = client.search_recent_tweets(
        query=query, max_results=100, user_auth=True, expansions="author_id"
    )
    users_id = random.choices(
        [user["id"] for user in tweets.includes["users"]], k=count
    )
    tweets_id = random.choices([tweet["id"] for tweet in tweets.data], k=count)
    for user_id, tweet_id in zip(users_id, tweets_id):
        client.like(tweet_id)
        client.follow_user(user_id)


@retry(tries=5, delay=5)
def tweet(client, driver):
    driver.get("https://twittrend.jp/")
    trend_list = [
        driver.find_element(By.XPATH, f"//li[{i}]/p/a").text for i in range(1, 21)
    ]
    picked_trend_1, picked_trend_2 = random.choices(trend_list, k=2)

    driver.get("https://www.pencil.elyza.ai/")
    driver.find_element(By.CSS_SELECTOR, '[placeholder="キーワード1[必須]"]').send_keys(
        remove_hashtag(picked_trend_1)
    )
    driver.find_element(By.CSS_SELECTOR, '[placeholder="キーワード2[必須]"]').send_keys(
        remove_hashtag(picked_trend_2)
    )
    driver.find_element(By.XPATH, "//input[@type='checkbox']").click()
    driver.find_element(By.XPATH, "//button[contains(.,'AI執筆スタート')]").click()
    wait = WebDriverWait(driver, 30)
    wait.until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//div[@id='result']/div[4]/div/div/p")
        )
    )
    result = driver.find_element(
        By.XPATH, "//div[@id='result']/div[4]/div/div/p").text
    tweet_content = (
        f"{result}\n{check_hashtag(picked_trend_1)}\n{check_hashtag(picked_trend_2)}"
    )

    client.create_tweet(text=tweet_content)


if __name__ == "__main__":
    # https://developers.whatismybrowser.com/useragents/explore/
    USER_AGENT_LISTS = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    ]

    CHROME_OPTION_LISTS = [
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--disable-web-security",
        "--disable-desktop-notifications",
        "--allow-running-insecure-content",
        "--ignore-certificate-errors",
        "--blink-settings=imagesEnabled=false",
        '--proxy-server="direct://"',
        "--disable-dev-shm-usage",
        "--proxy-bypass-list=*",
        "--start-maximized",
        "--kiosk",
    ]

    # https://www.youtube.com/watch?v=fD-GRCH_tks
    tweepy_client = tweepy.Client(
        consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret=os.environ['CONSUMER_SECRET'],
        access_token=os.environ['ACCESS_TOKEN'],
        access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
    )

    user_agent = USER_AGENT_LISTS[random.randrange(
        0, len(USER_AGENT_LISTS), 1)]

    arguments = [*CHROME_OPTION_LISTS, f"--user-agent={user_agent}"]

    options = Options()
    for argument in arguments:
        options.add_argument(argument)
    chrome_driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )

    tweet(tweepy_client, chrome_driver)

    like_follow_by_query(tweepy_client, "#繋がりたい #友達欲しい", 10)
