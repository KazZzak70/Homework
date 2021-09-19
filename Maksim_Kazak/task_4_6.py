from task_4_3 import split_analog


def get_longest_word(input_str: str = None) -> str:
    words_set = split_analog(input_str)
    max_len = 0
    max_word = str()
    for word in words_set:
        if word.__len__() > max_len:
            max_len = word.__len__()
            max_word = word
    return max_word


if __name__ == '__main__':
    example_str_1 = 'Python is simple and effective!'
    example_str_2 = 'Any pythonista like namespaces a lot.'
    print(f"Example string: {example_str_1}\n\tResult: {get_longest_word(example_str_1)}")
    print(f"Example string: {example_str_2}\n\tResult: {get_longest_word(example_str_2)}")
