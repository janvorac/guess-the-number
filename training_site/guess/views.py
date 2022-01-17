from random import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Game, Guessed

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'guess/index.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.filter(last_played_date__lte=timezone.now()).order_by('-last_played_date')[:5]


class GameView(generic.DetailView):
    model = Game
    template_name = 'guess/game.html'


def new_game(request):
    ng = Game(last_played_date=timezone.now(), correct_number=random.randint(0, 100))
    ng.save()
    return HttpResponseRedirect(reverse('guess:detail', args=(ng.id,)))


def new_guess(request, game_id):
    guessed_num = request.POST['num_guessed']
    if guessed_num:
        guessed_num = int(guessed_num)
        guessed = Guessed(game_id=game_id, number=guessed_num)
        guessed.save()
        current_game = get_object_or_404(Game, pk=game_id)
        if guessed_num == current_game.correct_number:
            current_game.finished = True
            current_game.save()
            return HttpResponseRedirect(reverse('guess:index'))  # todo: there should be a better redirect
    return HttpResponseRedirect(reverse('guess:detail', args=(game_id,)))


