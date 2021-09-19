def check_palindrome(input_str: str = None) -> bool:
    if input_str.__len__() % 2 == 1 and input_str is not None:
        str_len = input_str.__len__()
        for pos, symbol in enumerate(input_str.lower()):
            if pos == int((str_len - 1) / 2):
                return True
            if symbol == input_str.lower()[str_len - pos - 1]:
                continue
    else:
        return False


example_str = 'Kazak'
print(f"Example:\n\t{example_str}\nResult:\n\t{check_palindrome(example_str)}")
