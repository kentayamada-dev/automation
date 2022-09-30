from logging import Logger
from requests import post, get
from tenacity import retry, wait_fixed, stop_after_attempt


@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def post_with_error_handling(logger: Logger, url: str, params=None):
    log = f"URL    : {url}" f"\nParams : {params}"

    try:
        response = (
            post(url=url, timeout=(3.0, 9.0), params=params)
            if params is not None
            else post(url=url, timeout=(3.0, 9.0))
        )
        data = response.json()
        if response.status_code != 200:
            raise Exception(None)

        logger.error(log + f"\nData      : {data}")
    except Exception as exc:
        logger.critical(log + f"\nData      : {data}" + f"\nMessage   : {exc}")
        raise exc

    return data


@retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
def get_with_error_handling(logger: Logger, url: str):
    log = f"URL : {url}"

    try:
        response = get(url=url, timeout=(3.0, 9.0))
        data = response.json()

        logger.error(log + f"\nData      : {data}")
    except Exception as exc:
        logger.critical(log + f"\nMessage   : {exc}")
        raise exc

    return data
