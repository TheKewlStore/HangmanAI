import re

from base import PlayerInterface


class CheatingPlayer(PlayerInterface):
    def __init__(self, name, words):
        super(CheatingPlayer, self).__init__(name)

        self.all_words = words

    def get_letter_regex(self):
        letters_guessed = ''.join(self.incorrect_guesses) + ''.join(self.correct_guesses)

        if not letters_guessed:
            return '(.)'

        return '([^{0}])'.format(letters_guessed)

    def get_guess(self, current_letters):
        possible_words = self.all_words[len(current_letters)]
        possible_words_string = '\n'.join(possible_words).replace("'", '')
        pattern = re.compile(''.join(current_letters).replace('_', self.get_letter_regex()), re.MULTILINE)
        match = pattern.findall(possible_words_string)[0]
        return match[0]
