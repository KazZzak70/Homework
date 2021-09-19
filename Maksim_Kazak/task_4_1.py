def replace_quotes(input_str: str) -> str:
    if '\'' or '\"' in input_str:
        output_str = str()
        for symbol in input_str:
            if symbol == '\'':
                output_str += '\"'
            elif symbol == '\"':
                output_str += '\''
            else:
                output_str += symbol
        return output_str
    else:
        return 'There are no quotes in input string!'


example_str = 'the dog says \'Woof\', and the cat says \"Meow\"'
print(f"Before:\n\t{example_str}\nAfter:\n\t{replace_quotes(example_str)}")
