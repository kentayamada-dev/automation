# https://www.youtube.com/watch?v=Q5kw7vGLqgs
# https://di-acc2.com/system/rpa/19288/
# https://developers.facebook.com/tools/explorer/

from random import choice, sample
from json import dump, load
from os import environ
from requests import post, get
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from retry import retry
from chrome_driver import get_chrome_driver

BASE_URL = "https://graph.facebook.com/v15.0"
HASH_TAG_LIST = [
    "#photooftheday",
    "#instagood",
    "#nofilter",
    "#tbt",
    "#igers",
    "#picoftheday",
    "#love",
    "#nature",
    "#swag",
    "#lifeisgood",
    "#caseofthemondays",
    "#instapic",
    "#instadaily",
    "#selfie",
    "#instamood",
    "#bestoftheday",
    "#写真撮ってる人と繋がりたい",
    "#写真好きな人と繋がりたい",
    "#ファインダー越しの私の世界",
    "#かわいい",
    "#可愛い",
    "#インスタ映え",
    "#最高",
]
FAVORITE_LIST = [
    "573ca541-fbc1-47bf-9827-f4f781efeee6",
    "fad7742d-2b9b-4353-b8ae-aab6bc413336",
    "e226a552-7c8b-4ae4-ace6-ddb4ba971f19",
]


def save_post_data(permalink: str, timestamp: str, image_url: str):
    with open("instagram-post-data.json", "r", encoding="utf-8") as file:
        saved_data = load(file)
        file.close()
    new_data = {"timestamp": timestamp, "permalink": permalink, "image_url": image_url}
    saved_data.append(new_data)
    with open("instagram-post-data.json", "w", encoding="utf-8") as file:
        dump(saved_data, file, indent=2)
        file.close()


def post_image(image_url: str):
    hash_tags = (
        " ".join(sample(HASH_TAG_LIST, choice(range(5, 8)))) + " #legit_art_feed"
    )
    media_url = f"{BASE_URL}/{environ['INSTAGRAM_BUSINESS_ACCOUNT_ID']}"
    upload_url = f"{media_url}/media"
    publish_url = f"{media_url}/media_publish"
    upload_params = {
        "image_url": image_url,
        "caption": hash_tags,
        "access_token": environ["INSTAGRAM_ACCESS_TOKEN"],
    }
    upload_response = post(upload_url, timeout=(3.0, 9.0), params=upload_params)
    container_id = upload_response.json()["id"]
    publish_params = {
        "creation_id": container_id,
        "access_token": environ["INSTAGRAM_ACCESS_TOKEN"],
    }
    post_id = post(publish_url, timeout=(3.0, 9.0), params=publish_params).json()["id"]
    post_url = f"{BASE_URL}/{post_id}"
    post_params = {
        "access_token": environ["INSTAGRAM_ACCESS_TOKEN"],
        "fields": "permalink, timestamp",
    }
    post_data = get(post_url, timeout=(3.0, 9.0), params=post_params).json()
    return post_data


@retry(tries=5, delay=5)
def get_image():
    chrome_driver = get_chrome_driver()
    chrome_driver.get(f"https://lexica.art/?q={choice(FAVORITE_LIST)}")
    image = choice(chrome_driver.find_elements(By.TAG_NAME, "img"))
    chrome_driver.execute_script("arguments[0].scrollIntoView();", image)
    image.click()
    return image.get_attribute("src"), chrome_driver.current_url


if __name__ == "__main__":
    load_dotenv()
    image_src, generated_image_url = get_image()
    data = post_image(image_src)
    save_post_data(data["permalink"], data["timestamp"], generated_image_url)
