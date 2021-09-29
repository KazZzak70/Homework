import string


class Cipher:

    def __init__(self, keyword: str):
        self._keyword = sorted(set(keyword), key=keyword.index)
        self._secret_alphabet_dict = dict()
        for key, letter in enumerate(self._keyword):
            self._secret_alphabet_dict[string.ascii_lowercase[key]] = letter.lower()
            self._secret_alphabet_dict[string.ascii_uppercase[key]] = letter.upper()
        remaining_letters_normal = list(string.ascii_lowercase[len(self._keyword):])
        remaining_letters_secret = list(string.ascii_lowercase)
        for letter in self._keyword:
            if letter.lower() in remaining_letters_secret:
                remaining_letters_secret.remove(letter.lower())
        for key, letter in enumerate(remaining_letters_normal):
            self._secret_alphabet_dict[letter] = remaining_letters_secret[key]
            self._secret_alphabet_dict[letter.upper()] = remaining_letters_secret[key].upper()

    def encode(self, message: str) -> str:
        output_message = ''
        for letter in message:
            if letter == " ":
                output_message += " "
            else:
                output_message += self._secret_alphabet_dict[letter]
        return output_message

    def decode(self, message: str) -> str:
        output_message = ''
        for letter in message:
            if letter == " ":
                output_message += " "
                continue
            else:
                for item in self._secret_alphabet_dict.items():
                    if letter == item[1]:
                        output_message += item[0]
        return output_message


# if __name__ == "__main__":
#     cipher = Cipher('Crypto')
#     print(cipher.decode("Fjedhc dn atidsn"))
