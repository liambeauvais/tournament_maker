from django.http import HttpResponseRedirect
from django.shortcuts import render

from game.views import value_is_digit
from pool.models import Pool


# Create your views here.

def modify_table(request, *args, **kwargs):
    pool = Pool.objects.get(pk=kwargs['pk'])
    table = request.POST.get('table')

    if value_is_digit(table):
        pool.table = int(table)
        pool.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
