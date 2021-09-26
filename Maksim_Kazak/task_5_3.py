import csv
students_file_info = ["../data/students.csv", "r"]
students_sorted_file = ["../data/students_sorted.csv", "w"]


def get_top_performers(file_path, number_of_top_students=5):
    with open(file_path) as file_:
        students_list = list(csv.DictReader(file_))
        students_list = sorted(students_list, key=lambda a: a['average mark'], reverse=True)
        students_list = students_list[:number_of_top_students]
        for key, student in enumerate(students_list):
            students_list[key] = student['student name']
        print(students_list)


def sorted_by_age(input_file: list):
    with open(*input_file) as input_file:
        students_list = list(csv.DictReader(input_file))
        students_list = sorted(students_list, key=lambda a: a['age'])
        with open(*students_sorted_file) as output_file:
            writer = csv.DictWriter(output_file, ['student name', 'age', 'average mark'])
            writer.writeheader()
            writer.writerows(students_list)


if __name__ == "__main__":
    get_top_performers(students_file_info[0], 3)
    sorted_by_age(students_file_info)
