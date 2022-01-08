from django.test import TestCase

from .guesser import Guesser


class TestGuesser(TestCase):

    def setUp(self) -> None:
        self.guesser = Guesser(secret_number=50)

    def test_lower(self):
        message = self.guesser.guess(20)
        self.assertEqual("Too low!", message)

# Create your tests here.
