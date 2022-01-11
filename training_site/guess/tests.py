import django.test
import unittest

from training_site.guess.guesser import Guesser


class TestGuesser(unittest.TestCase):

    def setUp(self) -> None:
        self.guesser = Guesser(secret_number=50)

    def test_lower(self):
        message = self.guesser.guess(20)
        self.assertEqual("Too low!", message)

    def test_higher(self):
        message = self.guesser.guess(70)
        self.assertEqual("Too high!", message)

# Create your tests here.
