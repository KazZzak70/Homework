import time


def execution_time(f):
    def wrapper(*args, **kwargs):
        time_start = time.time()
        result = f(*args, **kwargs)
        time_finish = time.time()
        print(f"[INFO] Execution time is {round(time_finish - time_start, 3)} sec")
        return result
    return wrapper
