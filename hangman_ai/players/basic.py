from base import PlayerInterface


class BasicPlayer(PlayerInterface):
    def __init__(self, name):
        super(BasicPlayer, self).__init__(name)

        self.guess_order = ['a', 'e', 'i', 'o', 'u', 'y', 't', 's', 'n', 'r', 'h', 'l', 'd',
                            'c', 'm', 'f', 'p', 'g', 'w', 'b', 'v', 'k', 'x', 'j', 'q', 'z']

        self.number_of_guesses = 0

    def get_guess(self, current_letters):
        if self.number_of_guesses >= len(self.guess_order):
            self.number_of_guesses = 0

        this_guess = self.guess_order[self.number_of_guesses]
        self.number_of_guesses += 1

        return this_guess

    def reset(self):
        super(BasicPlayer, self).reset()
        self.number_of_guesses = 0
