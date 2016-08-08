import re


class GameLostException(Exception):
    pass


class GameWonException(Exception):
    pass


class PlayerInterface(object):
    def __init__(self, name):
        self.guesses = 0
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.name = name

    def correct_guess(self, guess):
        self.correct_guesses.append(guess)

    def incorrect_guess(self, guess):
        self.incorrect_guesses.append(guess)

    def get_guess(self, current_letters):
        raise NotImplementedError("This method needs to be implemented by subclasses")

    def reset(self):
        self.guesses = 0
        self.correct_guesses = []
        self.incorrect_guesses = []


class BasicPlayer(PlayerInterface):
    def __init__(self, name):
        super(BasicPlayer, self).__init__(name)

        self.guess_order = ['a', 'e', 'i', 'o', 'u', 'y', 't', 's', 'n', 'r', 'h', 'l', 'd',
                            'c', 'm', 'f', 'p', 'g', 'w', 'b', 'v', 'k', 'x', 'j', 'q', 'z']

        self.number_of_guesses = 0

    def get_guess(self, current_letters):
        this_guess = self.guess_order[self.number_of_guesses]
        self.number_of_guesses += 1
        return this_guess


class Game(object):
    def __init__(self, player):
        self.current_word = None
        self.current_letters = []
        self.max_guesses = 12
        self.player = player

    def start(self):
        self.current_word = str(raw_input("Enter a word, at least four characters: "))
        if len(self.current_word) < 4:
            print "Your word must have a least four characters!"
            return self.start_game()

        self.current_letters = ['_'] * len(self.current_word)

        while True:
            try:
                self.round()
            except GameLostException:
                return False
            except GameWonException:
                return True

    def round(self):
        if self.player.guesses >= self.max_guesses:
            raise GameLostException()

        letter_guessed = self.player.get_guess(self.current_letters)

        if len(letter_guessed) > 1 or not letter_guessed:
            print "Invalid guess, try again..."
            return

        if not self.check_guess(letter_guessed):
            self.player.guesses += 1
            print "{0} is not in the word, try again...".format(letter_guessed)
            return
        elif self.current_letters.count('_') == 0:
            raise GameWonException()
        else:
            print "{0} is in the word, current letters: {1}".format(letter_guessed, ''.join(self.current_letters))

    def check_guess(self, letter_guessed):
        if letter_guessed not in self.current_word:
            return False

        all_indexes = [match.start() for match in re.finditer(letter_guessed, self.current_word)]

        for index in all_indexes:
            self.current_letters[index] = letter_guessed

        return True


def main():
    basic_player = BasicPlayer('Ian')
    game = Game(basic_player)
    won = game.start()

    if won:
        print "You win! The word was {0}".format(game.current_word)
    else:
        print "You lost! The word was {0}".format(game.current_word)

if __name__ == "__main__":
    main()
