import logging as _logging
import time as _time
import requests as _requests


def execution_time(f):
    def wrapper(*args, **kwargs):
        time_start = _time.time()
        result = f(*args, **kwargs)
        time_finish = _time.time()
        print(f"Total execution time is {round(time_finish - time_start, 3)} sec")
        return result
    return wrapper


def network_exceptions_catcher(f):
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
            response.raise_for_status()
            return response
        except _requests.exceptions.ConnectTimeout:
            _logging.error(msg="Timed out.")
        except _requests.exceptions.ConnectionError:
            _logging.error(msg=f"HTTP Connection error, max retries exceeded")
        except _requests.exceptions.HTTPError as err:
            _logging.error(msg=f"{err}")
        except _requests.exceptions.ReadTimeout as err:
            _logging.error(msg=f"{err}")
    return wrapper
