import logging
import re
import sys

from hangman_ai import game_exceptions
from hangman_ai.players.basic import BasicPlayer
from hangman_ai.players.cheater import CheatingPlayer


logger = logging.getLogger()
logger.propagate = False

file_formatter = logging.Formatter('[%(levelname)s-%(asctime)s]: %(message)s',
                                   datefmt="%Y-%m-%d %H:%M:%S")

file_handler = logging.FileHandler('hangman_log.txt', mode='w')
stream_handler = logging.StreamHandler(sys.stdout)

file_handler.setFormatter(file_formatter)

logger.setLevel('DEBUG')
logger.addHandler(file_handler)


class Game(object):
    def __init__(self, player, current_word=None, max_guesses=12, print_messages=True):
        self.current_word = current_word
        self.current_letters = []
        self.max_guesses = max_guesses
        self.player = player
        self.print_messages = print_messages

        if print_messages:
            logger.addHandler(stream_handler)

    def prompt_for_word(self):
        self.current_word = str(raw_input("Enter a word, at least four characters: "))

        if len(self.current_word) < 4:
            logger.warning("Your word must have a least four characters!")
            return self.prompt_for_word()

    def start(self):
        if not self.current_word:
            self.prompt_for_word()

        self.current_letters = ['_'] * len(self.current_word)

        while True:
            try:
                self.round()
            except game_exceptions.GameLostException:
                return False
            except game_exceptions.GameWonException:
                return True

    def round(self):
        if self.player.guesses >= self.max_guesses:
            raise game_exceptions.GameLostException()

        letter_guessed = self.player.get_guess(self.current_letters)

        if len(letter_guessed) > 1 or not letter_guessed:
            if self.print_messages:
                logger.info("Invalid guess, try again...")

            return

        if not self.check_guess(letter_guessed):
            self.player.guesses += 1
            self.player.incorrect_guess(letter_guessed)

            if self.print_messages:
                logger.info("{0} is not in the word, try again...".format(letter_guessed))

            return
        elif self.current_letters.count('_') == 0:
            raise game_exceptions.GameWonException()
        else:
            self.player.correct_guess(letter_guessed)

            if self.print_messages:
                logger.info("{0} is in the word, current letters: {1}".format(letter_guessed, ''.join(self.current_letters)))

    def check_guess(self, letter_guessed):
        if letter_guessed not in self.current_word:
            return False

        all_indexes = [match.start() for match in re.finditer(letter_guessed, self.current_word)]

        for index in all_indexes:
            self.current_letters[index] = letter_guessed

        return True


class Simulation(object):
    def __init__(self, player, words, iterations=20):
        self.player = player
        self.words = words
        self.iterations = iterations
        self.win_statistics = {}
        self.total_games = {}

    def start(self):
        for iteration in xrange(1, self.iterations + 1):
            for word_length, words in self.words.iteritems():
                if word_length < 4:
                    continue

                for current_word in words:
                    game = Game(self.player, max_guesses=13, print_messages=False)

                    if not word_length in self.total_games:
                        self.total_games[len(current_word)] = 0

                    if not word_length in self.win_statistics:
                        self.win_statistics[word_length] = []

                    game.current_word = current_word
                    win = game.start()

                    logger.info(current_word + ' ' + str(win))

                    if win:
                        self.win_statistics[word_length].append(current_word)

                    self.total_games[word_length] += 1

                    self.player.reset()

    def print_statistics(self):
        for word_length, games_played in self.total_games.iteritems():
            games_won = len(self.win_statistics[word_length])
            percentage_won = (float(games_won) / float(games_played)) * 100
            logger.info("Win percentage for word length {0}: {1}% ({2} / {3})".format(word_length, percentage_won, games_won, games_played))


def words_by_length(words_filepath):
    sorted_words = {}

    with open(words_filepath, 'r') as words_file:
        for line in words_file:
            stripped_line = line.strip().replace("'", '')
            word_length = len(stripped_line)

            if not word_length in sorted_words:
                sorted_words[word_length] = []

            sorted_words[word_length].append(stripped_line)

    return sorted_words


def main():
    words = words_by_length('./words.txt')
    player = CheatingPlayer('Ian', './words.txt')
    simulation = Simulation(player, words, iterations=1)
    simulation.start()
    simulation.print_statistics()


if __name__ == "__main__":
    main()
