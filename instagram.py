# https://www.youtube.com/watch?v=Q5kw7vGLqgs
# https://di-acc2.com/system/rpa/19288/
# https://developers.facebook.com/tools/explorer/

import random
from random import choice, sample
# from datetime import datetime, timedelta, timezone
from os import environ
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from requests_with_error_handling import (
    post_with_error_handling,
)

BASE_URL = "https://graph.facebook.com/v15.0"
# CURRNET_HOUR_JST = datetime.now(timezone(timedelta(hours=+9), "JST")).hour
HASH_TAG_LIST = [
    "#instagood",
    "#drawing",
    "#art",
    "#love",
    "#fypシ",
    "#fyp",
    "#style",
    "#instapic",
    "#follow",
    "#beautiful",
    "#instamood",
    "#いいね返し",
    "#エモい",
    "#癒し",
    "#フォロー返し",
    "#イラスト",
    "#かわいい",
    "#可愛い",
    "#インスタ映え",
    "#最高",
    "#きれい",
]
# FAVORITE_LIST = {
#     "data_1": {
#         "time": [0, 5, 10, 15, 20],
#         "url": "https://lexica-serve-encoded-images2.sharif.workers.dev/md/d6ddce42-bfe7-4b18-b37c-e2fe2b9f786f",
#     },
#     "data_2": {
#         "time": [1, 6, 11, 16, 21],
#         "url": "https://lexica-serve-encoded-images2.sharif.workers.dev/md/df27f080-28a4-4ed0-bbcb-283e21f74e0a",
#     },
#     "data_3": {
#         "time": [2, 7, 12, 17, 22],
#         "url": "https://lexica-serve-encoded-images2.sharif.workers.dev/md/80a4b75e-64b1-4c15-a0a4-28029cf8a0b7",
#     },
#     "data_4": {
#         "time": [3, 8, 13, 18, 23],
#         "url": "https://lexica-serve-encoded-images2.sharif.workers.dev/md/0dd9bb0a-2722-49c0-9273-3c06b7942708",
#     },
#     "data_5": {
#         "time": [4, 9, 14, 19],
#         "url": "https://lexica-serve-encoded-images2.sharif.workers.dev/full_jpg/bdf9caf6-cfbf-4885-999c-f5091fe198e0",
#     },
# }


def post_image(image_url: str):
    hash_tags = (
        " ".join(sample(HASH_TAG_LIST, choice(range(8, 11))))
        + " #legit_art_feeds #ガチアート"
    )
    media_url = f"{BASE_URL}/{environ['INSTAGRAM_BUSINESS_ACCOUNT_ID']}"
    upload_url = f"{media_url}/media"
    publish_url = f"{media_url}/media_publish"
    upload_params = {
        "image_url": image_url,
        "caption": hash_tags,
        "access_token": environ["INSTAGRAM_ACCESS_TOKEN"],
    }
    container_id = post_with_error_handling(url=upload_url, params=upload_params)["id"]
    publish_params = {
        "creation_id": container_id,
        "access_token": environ["INSTAGRAM_ACCESS_TOKEN"],
    }
    post_with_error_handling(url=publish_url, params=publish_params)


# def get_image():
#     key = [k for k, v in FAVORITE_LIST.items() if CURRNET_HOUR_JST in v["time"]][0]
#     url = f"https://lexica.art/api/v1/search?q={FAVORITE_LIST[key]['url']}"
#     data = choice(
#         [
#             data
#             for data in get_with_error_handling(url=url)["images"]
#             if 320 < int(data["width"]) < 1440
#             # https://developers.facebook.com/docs/instagram-api/reference/ig-user/media/
#             and 0.8 < int(data["width"]) / int(data["height"]) < 1.91
#             and data["grid"] is False
#         ]
#     )

#     return data["src"]

def get_image() -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/usr/bin/google-chrome-stable"
        )
        page = browser.new_page()
        page.goto("https://www.fotor.com/images/inspiration")
        page.wait_for_timeout(3000)
        imgs = page.query_selector_all("img")
        img = random.choice([img.get_attribute("src") for img in imgs if img.get_attribute("src") and img.get_attribute("src").endswith(".src")])
        browser.close()
        return img or ""



if __name__ == "__main__":
    load_dotenv()
    image_data = get_image()
    post_image(image_data)
