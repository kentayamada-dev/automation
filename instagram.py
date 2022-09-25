# https://www.youtube.com/watch?v=Q5kw7vGLqgs
# https://di-acc2.com/system/rpa/19288/
# https://developers.facebook.com/tools/explorer/

from random import choice, sample
from datetime import datetime, timedelta, timezone
from json import dump, load
from os import environ
from dotenv import load_dotenv
from retry import retry
from requests_with_error_handling import (
    get_with_error_handling,
    post_with_error_handling,
)

BASE_URL = "https://graph.facebook.com/v15.0"
HASH_TAG_LIST = [
    "#可愛い",
    "#instagood",
    "#JKブランド",
    "#tbt",
    "#art",
    "#picoftheday",
    "#love",
    "#fypシ",
    "#fyp",
    "#jk",
    "#style",
    "#instapic",
    "#follow",
    "#beautiful",
    "#instamood",
    "#エモい",
    "#癒し",
    "#いいね返し",
    "#イラスト",
    "#かわいい",
    "#可愛い",
    "#インスタ映え",
    "#最高",
]
FAVORITE_LIST = {
    "data_1": {
        "time": [10, 14, 18, 22],
        "url": "https://image.lexica.art/md/aeaca738-b54e-4e3e-88d9-1b480d3e54fe",
    },
    "data_2": {
        "time": [11, 15, 19, 23],
        "url": "https://image.lexica.art/md/533d1efe-5326-4071-b23c-f7444f4700f9",
    },
    "data_3": {
        "time": [12, 16, 20],
        "url": "https://image.lexica.art/md/3028dc93-6ee9-4268-b8c6-e0280e4b4fb9",
    },
    "data_4": {
        "time": [13, 17, 21],
        "url": "https://image.lexica.art/md/09e02a01-9c99-45d7-bceb-c05fa5712adf",
    },
}
JST = timezone(timedelta(hours=+9), "JST")


def save_post_data(new_data: dict):
    with open("instagram-post-data.json", "r", encoding="utf-8") as file:
        saved_data = load(file)
        file.close()
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
    container_id = post_with_error_handling(url=upload_url, params=upload_params)["id"]
    publish_params = {
        "creation_id": container_id,
        "access_token": environ["INSTAGRAM_ACCESS_TOKEN"],
    }
    post_id = post_with_error_handling(url=publish_url, params=publish_params)["id"]
    post_url = f"{BASE_URL}/{post_id}"
    post_params = {
        "access_token": environ["INSTAGRAM_ACCESS_TOKEN"],
        "fields": "permalink, timestamp",
    }
    post_data = get_with_error_handling(post_url, params=post_params)
    return post_data


@retry(tries=5, delay=5)
def get_image():
    currnet_hour = datetime.now(JST).hour
    key = [k for k, v in FAVORITE_LIST.items() if currnet_hour in v["time"]][0]
    url = f"https://lexica.art/api/v1/search?q={FAVORITE_LIST[key]['url']}"
    data = choice(
        [
            data
            for data in get_with_error_handling(url)["images"]
            if 320 < int(data["width"]) < 1440
            # https://developers.facebook.com/docs/instagram-api/reference/ig-user/media/
            and 0.8 < int(data["width"]) / int(data["height"]) < 1.91
        ]
    )

    return data


if __name__ == "__main__":
    load_dotenv()
    image_data = get_image()
    post_image_response = post_image(image_data["src"])
    image_data["instagram_permalink"] = post_image_response["permalink"]
    image_data["instagram_timestamp"] = post_image_response["timestamp"]
    save_post_data(image_data)
