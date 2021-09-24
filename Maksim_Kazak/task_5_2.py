import re
from task_5_1 import files

input_file = ["../data/lorem_ipsum.txt", "r"]


@files(*input_file)
def most_common_words(file, number_of_words=3):
    data = file.readlines()
    word_dict = dict()
    for line in data:
        if line != '\n':
            line = re.findall(r'\w+', line.lower())
            for word in line:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
        else:
            continue
    sorted_word = sorted(word_dict.items(), key=lambda a: a[1])[::-1]
    return [a[0] for a in sorted_word[:number_of_words]]


if __name__ == "__main__":
    print(most_common_words(number_of_words=5))
