def get_digits(num: int) -> tuple[int]:
    return tuple(int(digit) for digit in str(num))


some_int = 87178291199
print(get_digits(num=some_int))
