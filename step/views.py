import math

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from player.models import Player
from pool.models import Pool, PoolPLayer
from step.functions.scoreboard import create_pool_scoreboard
from step.functions.step_generation import generate_pools
from step.models import Step
from tournament.models import Tournament


def create_first_step(request, *args, **kwargs):
    tournament = get_object_or_404(Tournament, id=kwargs.get('pk'))
    players_by_pool = int(request.POST.get('players'))
    print(request.POST)
    if tournament.step_set.count() == 0:
        players = tournament.players.order_by('-points').all()
        step = Step.objects.create(
            last_step=None,
            tournament_id=tournament.pk,
        )
        step.save()
        for player in players:
            step.players.add(player)
        step.save()

        numbers_of_pools = len(players) // players_by_pool + (1 if len(players) % players_by_pool != 0 else 0)

        generate_pools(numbers_of_pools, players, step.pk, players_by_pool)
    return redirect('steps', pk=tournament.pk)


def create_second_step(request, *args, **kwargs):
    first_step = get_object_or_404(Step, id=kwargs.get('pk'))
    ranks = {
        "1": [],
        "2": [],
        "3": []
    }
    for pool in first_step.pools.all():
        for pool_player in pool.players.all():
            ranks[str(pool_player.rank)].append(pool_player.player.pk)

    for rank, player_ids in ranks.items():
        step = Step.objects.create(
            last_step=first_step,
            tournament_id=first_step.tournament.pk,
            rank=int(rank)
        )
        step.save()
        players = Player.objects.filter(pk__in=player_ids).all()
        generate_pools(2, players, step.pk, math.ceil(float(len(players) / 2)))

    return redirect('second_steps', pk=first_step.tournament.pk)


def create_final_steps(request, *args, **kwargs):
    first_step = get_object_or_404(Step, id=kwargs.get('pk'))
    second_steps = first_step.step_set.all()
    for second_step in second_steps:
        ranks = {
        }
        for pool in second_step.pools.all():
            for pool_player in pool.players.all():
                if pool_player.rank in ranks:
                    ranks[pool_player.rank].append(pool_player.player.pk)
                else:
                    ranks[pool_player.rank] = [pool_player.player.pk]

        for rank, player_ids in ranks.items():
            step = Step.objects.create(
                last_step=second_step,
                tournament_id=first_step.tournament.pk,
                rank=int(rank)
            )
            step.save()
            players = Player.objects.filter(pk__in=player_ids).all()
            generate_pools(1, players, step.pk, 2)
    return redirect('final_steps', pk=first_step.tournament.pk)


class StepView(TemplateView):
    template_name = "step/step_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
        context['title'] = f"{first_step.tournament.date}-{first_step.tournament.get_category_display()}"

        context['step'] = first_step
        context['number_of_sets'] = [i + 1 for i in range(first_step.tournament.set_number)]
        return context


class SecondStepsView(TemplateView):
    template_name = "step/second_steps.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
        context['title'] = f"{first_step.tournament.date}-{first_step.tournament.get_category_display()}"

        second_steps = first_step.step_set.all()
        context["steps"] = second_steps
        context["firs_step"] = first_step
        context['number_of_sets'] = [i + 1 for i in range(first_step.tournament.set_number)]
        context['steps_are_done'] = all(step.is_done() for step in first_step.step_set.all())
        context['not_created'] = all(step.step_set.count() == 0 for step in first_step.step_set.all())
        return context


class FinalStepsView(TemplateView):
    template_name = 'step/final_steps.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
        context['title'] = f"{first_step.tournament.date}-{first_step.tournament.get_category_display()}"

        second_steps = first_step.step_set.all()
        context['tournament'] = first_step.tournament
        context["steps"] = second_steps
        context['number_of_sets'] = [i + 1 for i in range(first_step.tournament.set_number)]
        number_of_pools = 0
        for second_step in second_steps:
            for final_step in second_step.step_set.all():
                number_of_pools += final_step.pools.count()
        pool_number_list = []
        for i in range(1, number_of_pools + 1):
            pool_number_list.append(i * 2 - 1)
            pool_number_list.append(i * 2)
        context['counter'] = iter(pool_number_list)

        context['steps_are_done'] = all(
            step.is_done()
            for second_step in first_step.step_set.all()
            for step in second_step.step_set.all()
        )
        return context


def validate_pool(request, *args, **kwargs):
    pool = Pool.objects.get(pk=kwargs.get("pool_pk"))
    pool.validated = True
    pool.save()
    coeffs = create_pool_scoreboard(pool)
    sorted_coeffs = sorted(coeffs, key=lambda x: x['coeff'], reverse=True)
    count = 1
    for coef in sorted_coeffs:
        step_player = PoolPLayer.objects.get(player_id=coef['player_pk'], pool_id=pool.pk)
        step_player.rank = count
        step_player.coeff = coef['coeff']
        step_player.save()
        count += 1
    # return redirect('steps', pk=pool.step.tournament.pk)
    return redirect(request.META.get('HTTP_REFERER'))
