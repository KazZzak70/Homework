from string import ascii_lowercase


def characters_in_all(*args) -> set:
    if args is not None:
        characters_list = list()
        words_list = list()
        words_list.extend(args)
        first_word = words_list[0]
        del words_list[0]
        for letter in first_word:
            for word in words_list:
                if letter in word:
                    if word == words_list[words_list.__len__() - 1]:
                        characters_list.append(letter)
                    else:
                        continue
                else:
                    break
        return set(characters_list)


def characters_in_at_least_one(*args) -> set:
    if args is not None:
        characters_list = list()
        for word in args:
            for letter in word:
                if letter in characters_list:
                    continue
                else:
                    characters_list.append(letter)
        return set(characters_list)


def characters_in_at_least_two(*args):
    if args is not None:
        characters_list = list()
        words_list = list()
        words_list.extend(args)
        while words_list.__len__() >= 2:
            word_end = words_list.pop()
            for letter in word_end:
                for word in words_list:
                    if letter in word:
                        characters_list.append(letter)
        return set(characters_list)


def not_used_letters(*args):
    if args is not None:
        alphabet_string = ascii_lowercase
        alphabet_list = list(alphabet_string)
        for word in args:
            for letter in word:
                if letter in alphabet_list:
                    alphabet_list.remove(letter)
                else:
                    continue
        return set(alphabet_list)


if __name__ == "__main__":
    test_strings = ['hello', 'world', 'python']
    print(characters_in_all(*test_strings), end='\n')
    print(characters_in_at_least_one(*test_strings), end='\n')
    print(characters_in_at_least_two(*test_strings), end='\n')
    print(not_used_letters(*test_strings), end='\n')
