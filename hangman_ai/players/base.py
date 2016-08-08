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
