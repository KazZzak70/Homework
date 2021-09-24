unsorted_file = ["../data/unsorted_names.txt", "r"]
sorted_file = ["../data/sorted_names.txt", "w"]


def files(file_path, mode):
    def decorator(f):
        def wrapper(*args, **kwargs):
            with open(file_path, mode) as file:
                result = f(file, *args, **kwargs)
                return result
        return wrapper
    return decorator


def sorted_l(f):
    def wrapper(names_list: list, *args, **kwargs):
        names_list.sort()
        result = f(names_list, *args, **kwargs)
        return result
    return wrapper


@files(*unsorted_file)
def read_lines(file):
    names_list = file.readlines()
    return names_list


@sorted_l
@files(*sorted_file)
def write_lines(file, names_list: list):
    file.writelines(names_list)


if __name__ == "__main__":
    names_l = read_lines()
    write_lines(names_l)
