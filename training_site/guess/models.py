from django.db import models

# Create your models here.


class Game(models.Model):
    last_played_date = models.DateField('played on')

    def __str__(self):
        return f'played on {self.last_played_date}'


class Guessed(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return self.number
