from remember_result import remember_result


@remember_result
def sum_list(*args):
    result = ""
    for item in args:
        result += item
    print(f"Current result = '{result}'")
    return result


if __name__ == "__main__":
    sum_list("a", "z")
    sum_list("c", "d")
    sum_list("e", "f")
