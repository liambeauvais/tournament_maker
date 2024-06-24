from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from pool.models import Pool
from step.functions.scoreboard import create_or_update_scoreboard
from step.functions.step_generation import generate_pools
from step.models import Step, StepPLayer
from tournament.models import Tournament


def create_first_step(request, *args, **kwargs):
    tournament = get_object_or_404(Tournament, id=kwargs.get('pk'))
    if tournament.step_set.count() == 0:
        players = tournament.players.order_by('points').all()
        step = Step.objects.create(
            last_step=None,
            tournament_id=tournament.pk,
        )
        step.save()
        StepPLayer.objects.bulk_create(
            StepPLayer(
                step_id=step.pk,
                player_id=player.pk,
                rank=0
            ) for player in players
        )

        numbers_of_pools = len(players) // 3 + (1 if len(players) % 3 != 0 else 0)

        generate_pools(numbers_of_pools, players, step.pk, 3)
    return redirect('steps', pk=tournament.pk)


class StepView(TemplateView):
    template_name = "step/step_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
        context['step'] = first_step
        context['number_of_sets'] = [i + 1 for i in range(first_step.tournament.set_number)]
        return context


def validate_pool(request, *args, **kwargs):
    pool = Pool.objects.get(pk=kwargs.get("pool_pk"))
    pool.validated = True
    pool.save()
    create_or_update_scoreboard(pool)
    return redirect('steps', pk=pool.step.tournament.pk)
