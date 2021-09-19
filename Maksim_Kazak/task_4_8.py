def get_pairs(lst: list = None):
    if lst is not None and lst.__len__() != 1:
        output_str = list()
        pair = list()
        for elem in lst:
            if pair.__len__() == 1:
                pair.append(elem)
                first = elem
                output_str.append(tuple(pair))
                pair = [first]
            elif pair.__len__() == 0:
                pair.append(elem)
        return output_str
    else:
        return None


if __name__ == "__main__":
    examples_lst = [[1, 2, 3, 8, 9], ['need', 'to', 'sleep', 'more'], [1]]
    for example in examples_lst:
        print(f"Example list: {example}\nOutput list of tuples: {get_pairs(example)}\n")
