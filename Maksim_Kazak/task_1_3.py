some_string = str(input('Input the comma separated sequence of words:\n'))
words_list = list(set(some_string.split(', ')))
for word in words_list:
    print(word, end=', ' if not word == words_list[words_list.__len__() - 1] else '')
