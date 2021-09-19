def foo(index_lst: list[int]) -> list[int]:
    result = 1
    output_lst = list()
    for number in index_lst:
        result *= number
    for k in range(index_lst.__len__()):
        output_lst.append(int(result / index_lst[k]))
    return output_lst


if __name__ == "__main__":
    example_index_lst_1 = [1, 2, 3, 4, 5]
    example_index_lst_2 = [3, 2, 1]
    print(f"Example list: {example_index_lst_1}\nOutput: {foo(example_index_lst_1)}\n")
    print(f"Example list: {example_index_lst_2}\nOutput: {foo(example_index_lst_2)}")
