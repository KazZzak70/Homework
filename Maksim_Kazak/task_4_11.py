def combine_dict(*args) -> dict:
    if args is not None:
        result_dict = dict()
        for d in args:
            for item in d.items():
                if item[0] in result_dict:
                    result_dict[item[0]] += item[1]
                else:
                    result_dict[item[0]] = item[1]
        return result_dict


if __name__ == "__main__":
    dict_1 = {'a': 100, 'b': 200}
    dict_2 = {'a': 200, 'c': 300}
    dict_3 = {'a': 300, 'd': 100}
    print(f"dict_1: {dict_1}\ndict_2: {dict_2}\ndict_3: {dict_3}\n\n"
          f"combine dict_1, dict_2: {combine_dict(dict_1, dict_2)}\n\n"
          f"combine dict_1, dict_2, dict_3: {combine_dict(dict_1, dict_2, dict_3)}")
