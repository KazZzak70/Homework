

def sort_dict(unsorted_dict):
    sorted_dict = dict()
    for key in sorted(unsorted_dict.keys()):
        sorted_dict[key] = unsorted_dict[key]
    return sorted_dict


dict_numbers = {34: 1, 16: 4, 90: 8, 35: 3, 70: 14, 56: 45}
dict_letters = {'s': 23, 't': 56, 'w': 76, 'a': 10, 'k': 14}

print(f"Example with numbers:\n\tBefore sorting: {dict_numbers}\n\tAfter sorting: {sort_dict(dict_numbers)}")
print(f"Example with letters:\n\tBefore sorting: {dict_letters}\n\tAfter sorting: {sort_dict(dict_letters)}")
