from django.db import models

# Create your models here.


class Game(models.Model):
    last_played_date = models.DateField('played on')
    correct_number = models.IntegerField()
    finished = models.BooleanField(default=False)

    def __str__(self):
        ret = f'Game {self.id} ({self.last_played_date})'
        return ret

    def ordered_guess_set(self):
        return self.guessed_set.all().order_by('-id')


class Guessed(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)


