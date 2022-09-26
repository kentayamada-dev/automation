# https://www.youtube.com/watch?v=Q5kw7vGLqgs
# https://di-acc2.com/system/rpa/19288/
# https://developers.facebook.com/tools/explorer/

from random import choice, sample
from datetime import datetime, timedelta, timezone
from os import environ
from dotenv import load_dotenv
from retry import retry
from requests_with_error_handling import (
    get_with_error_handling,
    post_with_error_handling,
)

BASE_URL = "https://graph.facebook.com/v15.0"
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
FAVORITE_LIST = {
    "data_1": {
        "time": [0, 5, 10, 15, 20],
        "url": "https://image.lexica.art/md/c8db8b2f-8ce9-4a8b-8d70-c4a219864d0a",
    },
    "data_2": {
        "time": [1, 6, 11, 16, 21],
        "url": "https://image.lexica.art/md/45c5d8fc-714f-42db-83db-9fcc1d287f94",
    },
    "data_3": {
        "time": [2, 7, 12, 17, 22],
        "url": "https://image.lexica.art/md/22821a9b-9d3f-4343-9406-1693116ba1ff",
    },
    "data_4": {
        "time": [3, 8, 13, 18, 23],
        "url": "https://image.lexica.art/md/09e02a01-9c99-45d7-bceb-c05fa5712adf",
    },
    "data_5": {
        "time": [4, 9, 14, 19],
        "url": "https://image.lexica.art/md/f849963c-bf93-40df-aaa7-24f85092cf8a",
    },
}
JST = timezone(timedelta(hours=+9), "JST")


def post_image(image_url: str):
    hash_tags = (
        " ".join(sample(HASH_TAG_LIST, choice(range(10, 14)))) + " #legit_art_feed"
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
    post_image(image_data["src"])
