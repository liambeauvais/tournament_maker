from django.shortcuts import render, redirect

from game.models import Game
from game_set.models import Set


# Create your views here.
def value_is_digit(value):
    if not value:
        return False
    try:
        num = int(value)
        return True
    except ValueError:
        return False


def update_game(request, *args, **kwargs):
    game = Game.objects.get(pk=kwargs['pk'])
    print(request.POST)
    for key, value in request.POST.items():
        if key == "csrfmiddlewaretoken" or not value_is_digit(value):
            continue
        game_set = Set.objects.get(pk=key)
        game_set.score = int(value)
        game_set.save()
    return redirect('steps', game.tournament.pk)
