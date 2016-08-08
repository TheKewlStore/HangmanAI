import re

from base import PlayerInterface


class CheatingPlayer(PlayerInterface):
    def __init__(self, name, words_filepath):
        super(CheatingPlayer, self).__init__(name)

        self.all_words = self.all_words(words_filepath)

    def all_words(self, words_filepath):
        sorted_words = {}

        with open(words_filepath, 'r') as words_file:
            for line in words_file:
                stripped_line = line.strip()
                word_length = len(stripped_line)

                if not word_length in sorted_words:
                    sorted_words[word_length] = []

                sorted_words[word_length].append(stripped_line)

        return sorted_words

    def get_letter_regex(self):
        letters_guessed = ''.join(self.incorrect_guesses) + ''.join(self.correct_guesses)

        if not letters_guessed:
            return '(.)'

        return '([^{0}])'.format(letters_guessed)

    def get_guess(self, current_letters):
        possible_words = self.all_words[len(current_letters)]
        possible_words_string = '\n'.join(possible_words)
        pattern = re.compile(''.join(current_letters).replace('_', self.get_letter_regex()), re.MULTILINE)
        match = pattern.findall(possible_words_string)[0]
        return match[0]
