def split_by_index(s: str, indexes: list[int]) -> list[str]:
    w_begin = 0
    indexes.append(s.__len__())
    output_list = list()
    for index in indexes:
        if index not in range(0, s.__len__() + 1):
            indexes.remove(index)
        output_list.append(s[w_begin:index])
        w_begin = index
    return output_list


example_string = "pythoniscool,isn\'tit?"
indexes_list = [6, 8, 12, 13, 18]
print(split_by_index(example_string, indexes_list))
