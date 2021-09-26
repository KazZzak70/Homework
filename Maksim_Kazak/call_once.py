params_list = [None, None]


def call_once(f):
    def wrapper(a, b):
        global params_list
        if params_list == [None, None]:
            params_list = [a, b]
        result = f(*params_list)
        return result
    return wrapper
