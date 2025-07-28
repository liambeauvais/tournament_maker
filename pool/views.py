from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from game.views import value_is_digit
from pool.models import Pool, PoolPLayer


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


class PoolTieBreakerView(View):
    template_name = 'pool/pool_tiebreaker.html'
