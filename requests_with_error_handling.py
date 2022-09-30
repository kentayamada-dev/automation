from json import dumps
from requests import post, get
from tenacity import retry, wait_fixed, stop_after_attempt
from my_logger import my_logger


@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def post_with_error_handling(url: str, params=None):
    log = f"URL     : {url}"

    try:
        response = (
            post(url=url, timeout=(3.0, 9.0), params=params)
            if params is not None
            else post(url=url, timeout=(3.0, 9.0))
        )
        data = response.json()
        if response.status_code != 200:
            raise Exception(None)

        my_logger.error(log + f"\nData    :\n{dumps(data, indent=2)}")
    except Exception as exc:
        my_logger.critical(
            log + f"\nData    :\n{dumps(data, indent=2)}" + f"\nMessage : {exc}"
        )
        raise exc

    return data


@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def get_with_error_handling(url: str):
    log = f"URL  : {url}"

    try:
        response = get(url=url, timeout=(3.0, 9.0))
        data = response.json()

        my_logger.error(log + f"\nData :\n{dumps(data, indent=2)}")
    except Exception as exc:
        my_logger.critical(log + f"\nMessage : {exc}")
        raise exc

    return data
