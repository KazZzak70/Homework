last_call_result = None


def remember_result(f):
    def wrapper(*args):
        global last_call_result
        print(f"Last result = '{last_call_result}'")
        result = f(*args)
        last_call_result = result
    return wrapper