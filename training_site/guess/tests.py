import django.test
from django.urls import reverse
from django.utils import timezone
from .models import Game, Guessed
# Create your tests here.


class GamesIndexViewTests(django.test.TestCase):
    def test_no_games(self):
        response = self.client.get(reverse('guess:index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No open games available. Start playing!")
        self.assertContains(response, "No closed games available. You must guess that number!")

    def test_one_unfinished_game(self):
        game = Game.objects.create(last_played_date=timezone.now(), correct_number=50)
        response = self.client.get(reverse('guess:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['unfinished_games'], [game])
        self.assertQuerysetEqual(response.context['finished_games'], [])

    def test_one_finished_game(self):
        game = Game.objects.create(last_played_date=timezone.now(), correct_number=50)
        guess = Guessed.objects.create(game_id=game.id, number=50)
        game.finished = True
        game.save()
        response = self.client.get(reverse('guess:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['unfinished_games'], [])
        self.assertQuerysetEqual(response.context['finished_games'], [game])
