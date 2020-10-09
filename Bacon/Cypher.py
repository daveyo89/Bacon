import re

lookup = {'A': 'bbbbb', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
          'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
          'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
          'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
          'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 'Z': 'bbaab'}


class BaconSpider:
    def __init__(self, cover_poetry, secret_message):
        self.lookup = lookup

        self.cover_poetry = cover_poetry
        self.poetry_list = cover_poetry.replace(',', ' ,').replace(';', ' ;').replace("\n", ' \\n ').lower().split()
        self.secret_message = secret_message

    def to_binary(self):
        binaries = []
        for char in self.secret_message.upper():
            for i, j in self.lookup.items():
                if char == i:
                    binaries.append(j)
        setattr(self, 'binaries', binaries)

    def to_be_encoded(self):
        to_encode = dict()

        for i in range(len(self.poetry_list)):
            word = self.poetry_list[i]
            if len(word) >= 5:
                to_encode[i] = word
        setattr(self, 'to_encode', to_encode)

    def make_it_upper(self):
        binaries = self.binaries
        words_to_change = self.to_encode
        result = dict()
        all_words = iter(words_to_change.items())
        for i in range(len(binaries)):
            binary_word = binaries[i]
            next_word = next(all_words)
            new_word = ""
            for char_index in range(len(binary_word)):
                char = binary_word[char_index]
                if char == 'b':
                    new_word += next_word[1][char_index].upper()
                else:
                    new_word += next_word[1][char_index]
            new_word += next_word[1][char_index + 1::]
            result.update(dict({next_word[0]: new_word}))

        setattr(self, 'make_it_upper_result', result)

    def encode_in_poem(self):
        coded_dict = self.make_it_upper_result
        poem = self.poetry_list

        for i, j in coded_dict.items():
            poem[i] = j

        result = " ".join(poem).replace(' ,', ',').replace(' ;', ';').replace('\\n', '\n').replace(' \n ',
                                                                                                   '\n').replace('\n ',
                                                                                                                 '\n')
        setattr(self, 'encode_in_poem_result', result)


class DecodeBaconSpider:
    def __init__(self, coded_poem):
        self.coded_poem = coded_poem
        self.lookup = lookup

    def get_code_words(self):
        code_words = [(re.search(r".*[A-Z]\S+", x)) for x in self.coded_poem.split() if len(x) >= 5]
        code_words = [x.group(0) for x in code_words if x is not None]

        setattr(self, 'code_words', code_words)

    def get_letters(self):
        coded_words = self.code_words
        result = []

        for e in coded_words:
            new = ["a"] * 5
            for i in range(5):
                if e[i].isupper():
                    new[i] = 'b'
            result.append("".join(new))

        setattr(self, 'get_letters_result', result)

    def translate(self):
        coded_letters = self.get_letters_result
        library = self.lookup
        result = []
        for cl in coded_letters:
            for key, value in library.items():
                if cl == value:
                    result.append(key)

        setattr(self, 'translate_result', " ".join(result))
