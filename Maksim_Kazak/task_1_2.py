from pprint import pprint

some_string = str(input('Input some string to count unique characters:\n'))
characters_dict = dict()
for symbol in some_string:
    if symbol not in characters_dict:
        characters_dict[symbol] = 1
    else:
        characters_dict[symbol] += 1
pprint(characters_dict)
