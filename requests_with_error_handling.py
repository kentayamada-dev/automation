from pprint import pprint
from typing import Any
from requests import post, get


def print_error_log(url: str, response: Any, exception_message: str):
    print("\n-----------------------------")
    print(f"URL:\n{url}")
    print("\nResponse:")
    pprint(response)
    print(f"\nError Message:\n{exception_message}")
    print("-----------------------------")


def post_with_error_handling(url: str, params=None):
    data = None
    try:
        response = (
            post(url=url, timeout=(3.0, 9.0), params=params)
            if params is not None
            else post(url=url, timeout=(3.0, 9.0))
        )
        data = response.json()
        if response.status_code != 200:
            raise Exception(None)
    # pylint: disable=broad-except
    except Exception as exception_message:
        print_error_log(url, data, exception_message)

    return data


def get_with_error_handling(url: str, params=None):
    data = None
    try:
        response = (
            get(url=url, timeout=(3.0, 9.0), params=params)
            if params is not None
            else get(url=url, timeout=(3.0, 9.0))
        )
        data = response.json()
    # pylint: disable=broad-except
    except Exception as exception_message:
        print_error_log(url, data, exception_message)

    return data
