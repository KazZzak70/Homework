from requests.exceptions import ConnectTimeout, ConnectionError, HTTPError, ReadTimeout
import functools
import logging
import time


def execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        print(f"Total execution time is {round(time.monotonic() - start_time, 3)} sec")
        return result
    return wrapper


def network_exceptions_catcher(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
        except ConnectTimeout:
            logging.error(msg="Timed out.")
        except ConnectionError:
            logging.error(msg=f"HTTP Connection error, max retries exceeded")
        except (HTTPError, ReadTimeout) as err:
            logging.error(msg=f"{err}")
        else:
            return response
    return wrapper
