import math

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from game.views import value_is_digit
from player.models import Player
from pool.models import Pool, PoolPLayer
from step.functions.scoreboard import create_pool_scoreboard, PlayerForSettle
from step.functions.step_generation import generate_pools
from step.models import Step
from tournament.functions.pdf import get_tournament_steps
from tournament.models import Tournament
from tournament.views import TournamentMixin


def create_first_step(request, *args, **kwargs):
    tournament = get_object_or_404(Tournament, id=kwargs.get('pk'))
    players_by_pool = int(request.POST.get('players'))
    set_number = int(request.POST.get('set_number'))

    if tournament.step_set.count() == 0:
        players = tournament.players.order_by('-points').all()
        step = Step.objects.create(
            last_step=None,
            tournament_id=tournament.pk,
            set_number=set_number,
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
    set_number = int(request.POST.get('set_number'))
    ranks = {}
    for pool in first_step.pools.all():
        for pool_player in pool.players.all():
            if pool_player.rank in ranks:
                ranks[pool_player.rank].append(pool_player.player.pk)
            else:
                ranks[pool_player.rank] = [pool_player.player.pk]

    for rank, player_ids in ranks.items():
        step = Step.objects.create(
            last_step=first_step,
            tournament_id=first_step.tournament.pk,
            rank=int(rank),
            set_number=set_number,
        )
        step.save()
        players = Player.objects.filter(pk__in=player_ids).all()
        generate_pools(2, players, step.pk, math.ceil(float(len(players) / 2)))

    return redirect('second_steps', pk=first_step.tournament.pk)


def create_final_steps(request, *args, **kwargs):
    first_step = get_object_or_404(Step, id=kwargs.get('pk'))
    set_number = int(request.POST.get('set_number'))
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
                rank=int(rank),
                set_number=set_number
            )
            step.save()
            players = Player.objects.filter(pk__in=player_ids).all()
            generate_pools(1, players, step.pk, 2)
    return redirect('final_steps', pk=first_step.tournament.pk)


class StepView(TemplateView, TournamentMixin):
    template_name = "step/step_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.get_tournament(**kwargs)
        first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
        context['title'] = f"{first_step.tournament.date}-{first_step.tournament.get_category_display()}"
        context['step'] = first_step
        context['first_step'] = first_step
        context['step_iteration'] = 1
        context['step_title'] = "Premières poules"
        context['next_steps_title'] = "deuxièmes poules"
        context['next_step_create_url'] = "create_second_step"
        context['next_step_url'] = 'second_steps'
        context['no_next_steps'] = first_step.step_set.count() == 0
        context['number_of_sets'] = [i + 1 for i in range(first_step.set_number)]

        pool_id_to_show = self.request.GET.get('show', 0)
        context['pool_id_to_show'] = int(pool_id_to_show)
        return context


class SecondStepsView(TemplateView, TournamentMixin):
    template_name = "step/second_steps.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.get_tournament(**kwargs)
        first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
        context['title'] = f"{first_step.tournament.date}-{first_step.tournament.get_category_display()}"

        second_steps = first_step.step_set.all()
        context["steps"] = second_steps
        context["first_step"] = first_step
        context['number_of_sets'] = [i + 1 for i in range(context["steps"][0].set_number)]
        context['steps_are_done'] = all(step.is_done() for step in first_step.step_set.all())

        context['step_iteration'] = 2
        context['step_title'] = "Deuxièmes poules"
        context['next_steps_title'] = "tableau final"
        context['next_step_create_url'] = "create_final_steps"
        context['next_step_url'] = "final_steps"
        context['no_next_steps'] = all(step.step_set.count() == 0 for step in first_step.step_set.all())

        pool_id_to_show = self.request.GET.get('show', 0)
        context['pool_id_to_show'] = int(pool_id_to_show)
        return context


class FinalStepsView(TemplateView, TournamentMixin):
    template_name = 'step/final_steps.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.get_tournament(**kwargs)
        first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
        context['title'] = f"{first_step.tournament.date}-{first_step.tournament.get_category_display()}"

        second_steps = first_step.step_set.all()
        context['tournament'] = first_step.tournament
        context['first_step'] = first_step
        context["steps"] = second_steps
        context['number_of_sets'] = [i + 1 for i in range(context["steps"][0].set_number)]
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

        context['step_iteration'] = 3
        context['step_title'] = "Phase finale"
        context['next_steps_title'] = "tableau final"
        context['next_step_create_url'] = "create_scoreboard"
        context['next_step_url'] = "scoreboard"
        context['no_next_steps'] = all(
            step.step_set.count() == 0
            for second_step in first_step.step_set.all()
            for step in second_step.step_set.all()
        )

        return context


def validate_pool(request, *args, **kwargs):
    pool = Pool.objects.get(pk=kwargs.get("pool_pk"))
    scoreboard: list[PlayerForSettle] = create_pool_scoreboard(pool)
    count = 1
    for player in scoreboard:
        pool_player = PoolPLayer.objects.get(player_id=player.id, pool_id=pool.pk)
        pool_player.rank = count
        pool_player.coeff = player.coefficient
        pool_player.save()
        count += 1
    return redirect(request.META.get('HTTP_REFERER'))


def force_pool_validation(request, *args, **kwargs):
    for key, value in request.POST.items():
        if key == "csrfmiddlewaretoken":
            continue
        pool_player = PoolPLayer.objects.get(pk=int(key))
        if value_is_digit(value):
            pool_player.rank = value
            pool_player.coeff = 0.0
            pool_player.save()
    return redirect(request.META.get('HTTP_REFERER'))


def cancel_steps(request, *args, **kwargs):
    tournament = Tournament.objects.get(pk=kwargs.get("pk"))
    first_step = Step.objects.filter(tournament=tournament).exclude(last_step__isnull=False).first()
    step_iteration = kwargs.get('step_iteration')
    steps = get_tournament_steps(first_step, step_iteration)
    for step in steps:
        step.delete()

    return redirect('tournament_detail', tournament.pk)
