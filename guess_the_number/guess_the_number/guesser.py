import random
from typing import Optional


class Guesser:

    def __init__(self, secret_number: Optional[int] = None):
        self._secret_number = secret_number or random.randint(0, 100)

    def guess(self, number: int):
        if number == self._secret_number:
            return "Correct!"
        elif number < self._secret_number:
            return "Too low!"
        elif number > self._secret_number:
            return "Too high!"
        else:
            raise ValueError(f"{number} is not a valid input.")
