
def find_unique(list_of_data):
    unique_values_set = set()
    for dict_ in list_of_data:
        for item in dict_.values():
            unique_values_set.add(item)
    return unique_values_set


example_list = [{"V": "S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII": "S005"}, {"V": "S009"},
                {"VIII": "S007"}]
print(find_unique(example_list))
