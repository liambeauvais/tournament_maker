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
    game_set = None
    for key, value in request.POST.items():
        if key == "csrfmiddlewaretoken":
            continue
        game_set = Set.objects.get(pk=key)
        if not value_is_digit(value):
            game_set.score = None
            game_set.save()
        else:
            game_set.score = int(value)
            game_set.save()

    referer_url = request.META.get('HTTP_REFERER', '/')
    if 'show' in referer_url:
        referer_url = referer_url.split('=')
        referer_url = f"{referer_url[0]}={game_set.game.pool.id}#accordion{game_set.game.pool.id}"
    else:
        referer_url = f'{referer_url}?show={game_set.game.pool.id}#accordion{game_set.game.pool.id}'
    return redirect(referer_url, {"show": game_set.game.pool.id})
