import csv
import logging
import re
import sys

from hangman_ai import game_exceptions
from hangman_ai.words import words_by_length
from hangman_ai.players.basic import BasicPlayer
from hangman_ai.players.cheater import CheatingPlayer


logger = logging.getLogger()
logger.propagate = False

file_formatter = logging.Formatter('[%(levelname)s-%(asctime)s]: %(message)s',
                                   datefmt="%Y-%m-%d %H:%M:%S")

file_handler = logging.FileHandler('hangman_log.txt', mode='w')
stream_handler = logging.StreamHandler(sys.stdout)

file_handler.setFormatter(file_formatter)

logger.setLevel('INFO')
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
            failed_words = 0

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

                    logger.debug(current_word + ' ' + str(win))

                    if win:
                        self.win_statistics[word_length].append(current_word)
                    else:
                        failed_words += 1

                    self.total_games[word_length] += 1

                    self.player.reset()

            logger.info('AI fails for {0} words'.format(failed_words))

    def statistics(self):
        for word_length, games_played in sorted(self.total_games.iteritems()):
            games_won = len(self.win_statistics[word_length])
            percentage_won = (float(games_won) / float(games_played)) * 100
            yield {'word_length': word_length,
                    'games_played': games_played,
                    'games_won': games_won,
                    'percentage_won': percentage_won,
                    }

    def print_statistics(self):
        for statistic in self.statistics():
            word_length = statistic['word_length']
            percentage_won = statistic['percentage_won']
            games_won = statistic['games_won']
            games_played = statistic['games_played']
            logger.info("Win percentage for word length {0}: {1}% ({2} / {3})".format(word_length, percentage_won, games_won, games_played))


def main():
    words = words_by_length(words_filepath='./resources/words2.txt')

    logger.info('Basic frequency based AI:')
    player = BasicPlayer('Ian')
    simulation = Simulation(player, words, iterations=1)
    simulation.start()
    basic_statistics = simulation.statistics()

    logger.info('Regex based word-bank sniffer AI:')
    player = CheatingPlayer('Ian', words)
    simulation = Simulation(player, words, iterations=1)
    simulation.start()
    cheating_statistics = simulation.statistics()

    with open('./statistics.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(['', 'Basic', 'Cheating'])

        for basic_statistic, cheating_statistic in zip(basic_statistics, cheating_statistics):
            word_length = basic_statistic['word_length']

            if not word_length == cheating_statistic['word_length']:
                continue

            basic_percentage = basic_statistic['percentage_won']
            cheating_percentage = cheating_statistic['percentage_won']

            writer.writerow([word_length, basic_percentage, cheating_percentage])

if __name__ == "__main__":
    main()
