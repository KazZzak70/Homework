def split_analog(input_str: str = None, sep: str = ' ') -> list:
    if input_str is not None:
        output_set = list()
        input_str = input_str.replace(sep, ',')
        w_start = 0
        for pos, symbol in enumerate(input_str):
            if symbol == ',' or pos == input_str.__len__() - 1:
                if pos == input_str.__len__() - 1:
                    pos += 1
                output_set.append(input_str[w_start:pos])
                w_start = pos + 1
        return output_set


if __name__ == '__main__':
    example_str = 'One Two Three Shot'
    print(split_analog(example_str))
