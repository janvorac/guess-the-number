import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Game, Guessed

import plotly.graph_objects as go

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'guess/index.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.filter(last_played_date__lte=timezone.now()).order_by(
            '-last_played_date'
        )[:5]

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, *kwargs)
        context['finished_games'] = Game.objects.filter(finished=True).order_by(
            '-last_played_date'
        )[:8]
        context['unfinished_games'] = Game.objects.filter(finished=False).order_by(
            '-last_played_date'
        )
        return context


class GameView(generic.DetailView):
    model = Game
    template_name = 'guess/game.html'


class InspectView(generic.DetailView):
    model = Game
    template_name = 'guess/inspect.html'

    @staticmethod
    def create_plot(ys, correct):
        trace = go.Scatter(y=ys, name='guesses')
        layout = go.Layout(
            title='Guess history', xaxis={'title': 'round'}, yaxis={'title': 'Guessed number'}
        )
        fig = go.Figure(data=[trace], layout=layout)
        fig.add_hline(y=correct)
        fig.add_annotation(x=0, y=correct, showarrow=False, text='Correct value', yshift=10)
        return fig

    def get_context_data(self, **kwargs):
        context = super(InspectView, self).get_context_data(**kwargs)
        game = context['object']
        context['plot'] = self.create_plot(
            ys=[int(guessed.number) for guessed in game.guessed_set.all()],
            correct=game.correct_number,
        ).to_html()

        return context


def new_game(request):
    ng = Game(last_played_date=timezone.now().date(), correct_number=random.randint(0, 100))
    ng.save()
    return HttpResponseRedirect(reverse('guess:detail', args=(ng.id,)))


def new_guess(request, game_id):
    guessed_num = request.POST['num_guessed']
    guess_feedback = ''
    if guessed_num:
        guessed_num = int(guessed_num)
        guessed = Guessed(game_id=game_id, number=guessed_num)
        guessed.save()
        current_game = get_object_or_404(Game, pk=game_id)
        current_game.last_played_date = timezone.now().date()
        if guessed_num == current_game.correct_number:
            current_game.finished = True
            current_game.save()
            return HttpResponseRedirect(
                reverse('guess:inspect', args=(current_game.id,))
            )
        elif guessed_num < current_game.correct_number:
            guess_feedback = 'Too low! Shoot higher.'
        elif guessed_num > current_game.correct_number:
            guess_feedback = 'Too high! Shoot lower.'

    return render(
        request,
        'guess/game.html',
        context={'guess_feedback': guess_feedback, 'game': current_game},
    )
