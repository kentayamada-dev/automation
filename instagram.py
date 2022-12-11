# https://www.youtube.com/watch?v=Q5kw7vGLqgs
# https://di-acc2.com/system/rpa/19288/
# https://developers.facebook.com/tools/explorer/

from random import choice, sample
from datetime import datetime, timedelta, timezone
from os import environ
from dotenv import load_dotenv
from requests_with_error_handling import (
    get_with_error_handling,
    post_with_error_handling,
)

BASE_URL = "https://graph.facebook.com/v15.0"
CURRNET_HOUR_JST = datetime.now(timezone(timedelta(hours=+9), "JST")).hour
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
        "url": "https://image.lexica.art/md/8f20b560-dc75-43b3-bbbf-636592a06b0b",
    },
    "data_2": {
        "time": [1, 6, 11, 16, 21],
        "url": "https://image.lexica.art/md/00abb491-93dd-423e-952a-f47660e74835",
    },
    "data_3": {
        "time": [2, 7, 12, 17, 22],
        "url": "https://image.lexica.art/md/62929e7a-8433-4f37-b3e6-2e311aa0f3e8",
    },
    "data_4": {
        "time": [3, 8, 13, 18, 23],
        "url": "https://image.lexica.art/md/2ab6bd98-cb1a-4d8e-b7bf-a9453398985e",
    },
    "data_5": {
        "time": [4, 9, 14, 19],
        "url": "https://image.lexica.art/md/032c6023-0d6b-4fc3-9ec8-a0102f0a11b2",
    },
}


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


def get_image():
    key = [k for k, v in FAVORITE_LIST.items() if CURRNET_HOUR_JST in v["time"]][0]
    url = f"https://lexica.art/api/v1/search?q={FAVORITE_LIST[key]['url']}"
    data = choice(
        [
            data
            for data in get_with_error_handling(url=url)["images"]
            if 320 < int(data["width"]) < 1440
            # https://developers.facebook.com/docs/instagram-api/reference/ig-user/media/
            and 0.8 < int(data["width"]) / int(data["height"]) < 1.91
            and data["grid"] is False
        ]
    )

    return data


if __name__ == "__main__":
    load_dotenv()
    image_data = get_image()
    post_image(image_data["src"])
