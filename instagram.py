# https://www.youtube.com/watch?v=Q5kw7vGLqgs
# https://di-acc2.com/system/rpa/19288/
# https://developers.facebook.com/tools/explorer/

from random import choice, sample
from json import dump, load
from os import environ
from requests import post, get
from dotenv import load_dotenv
from retry import retry

BASE_URL = "https://graph.facebook.com/v15.0"
HASH_TAG_LIST = [
    "#photooftheday",
    "#instagood",
    "#JKブランド"
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
    "#selfie",
    "#instamood",
    "#エモい",
    "#写真撮ってる人と繋がりたい",
    "#写真好きな人と繋がりたい",
    "#ファインダー越しの私の世界",
    "#かわいい",
    "#可愛い",
    "#インスタ映え",
    "#最高",
]
FAVORITE_LIST = [
    "https://images.unsplash.com/photo-1533109721025-d1ae7ee7c1e1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80",
    "https://image.lexica.art/md/533d1efe-5326-4071-b23c-f7444f4700f9",
    "https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
    "https://images.unsplash.com/photo-1601042879364-f3947d3f9c16?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80"
]


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
    try:
        upload_response = post(upload_url, timeout=(3.0, 9.0), params=upload_params)
        container_id = upload_response.json()["id"]
    # pylint: disable=broad-except
    except Exception as exception_message:
        print(f"Response: {upload_response.json()}\nError Message: {exception_message}")
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
    data = choice(
        [
            data
            for data in get(
                f"https://lexica.art/api/v1/search?q={choice(FAVORITE_LIST)}",
                timeout=(3.0, 9.0),
            ).json()["images"]
            if 320 < int(data["width"]) < 1440
        ]
    )

    return data


if __name__ == "__main__":
    load_dotenv()
    image_data = get_image()
    post_response = post_image(image_data["src"])
    image_data["instagram_permalink"] = post_response["permalink"]
    image_data["instagram_timestamp"] = post_response["timestamp"]
    save_post_data(image_data)
