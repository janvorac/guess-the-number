from django.http import HttpResponseRedirect
from django.shortcuts import render
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
    ng = Game(last_played_date=timezone.now())
    ng.save()
    return HttpResponseRedirect(reverse('guess:detail', args=(ng.id,)))


def new_guess(request, game_id):
    guessed_num = request.POST['num_guessed']
    if guessed_num:
        guessed = Guessed(game_id=game_id, number=guessed_num)
        guessed.save()
    return HttpResponseRedirect(reverse('guess:detail', args=(game_id,)))


