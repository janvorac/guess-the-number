from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from .models import Game, Guessed

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'guess/index.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.filter(date__lte=timezone.now()).order_by('-date')[:5]
