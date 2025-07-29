from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from player.models import Player
from pool.models import Pool, PoolPLayer
from step.functions.step_generation import generate_pools


# Create your views here.

def modify_table(request, *args, **kwargs):
    pool = Pool.objects.get(pk=kwargs['pk'])
    table = request.POST.get('table')

    pool.table = table
    pool.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_player_from_pool(request, *args, **kwargs):
    player_id = request.POST.get('player_id')
    pool_player = PoolPLayer.objects.get(pk=player_id)
    pool_player.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_player(request, *args, **kwargs):
    if request.method == 'GET':
        pool = Pool.objects.get(pk=kwargs['pk'])
        players = Player.objects.all().order_by('last_name')
        return render(request, 'pool/update.html', {'players': players, 'pool': pool})
    else:
        old_pool = Pool.objects.get(pk=kwargs['pk'])
        player_id = request.POST.get('player_id')
        pool_players = old_pool.players.all()

        players_ids = [pool_player.player.pk for pool_player in pool_players] + [int(player_id)]
        players = Player.objects.filter(pk__in=players_ids).all()

        step_pk = old_pool.step.pk
        generate_pools(1, players, step_pk, len(players))

        old_pool.delete()

        return render(request, 'pool/update.html', context={'player_added': True})
