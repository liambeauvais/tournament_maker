from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from scoreboard.models import Scoreboard, ScoreboardPlayer
from step.models import Step
from tournament.models import Tournament


# Create your views here.

def create_scoreboard(request, *args, **kwargs):
    tournament = Tournament.objects.get(pk=kwargs['pk'])
    scoreboard = Scoreboard(tournament=tournament)
    scoreboard.save()

    count = 1
    first_step: Step = Step.objects.filter(tournament_id=kwargs.get("pk")).exclude(last_step__isnull=False).first()
    for second_step in first_step.step_set.all().order_by('rank'):
        for final_step in second_step.step_set.all().order_by('rank'):
            for pool in final_step.pools.all():
                for pool_player in pool.players.all().order_by('rank'):
                    scoreboard_player = ScoreboardPlayer(
                        scoreboard=scoreboard,
                        player=pool_player.player,
                        rank=count
                    )
                    scoreboard_player.save()
                    count += 1
    return redirect('scoreboard', pk=tournament.pk)


class ScoreBoardView(TemplateView):
    template_name = "scoreboard/scoreboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = Tournament.objects.get(pk=self.kwargs['pk'])
        context["tournament"] = tournament
        context['title'] = f"{tournament.date}-{tournament.get_category_display()}"
        return context
