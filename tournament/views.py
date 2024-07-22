from django import forms
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView

from player.models import Player
from step.models import Step
from .functions.pdf import get_tournament_steps, get_steps_pools, render_to_pdf
from .models import Tournament, CATEGORIES, TOURNAMENT_TYPES


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['date', 'name', 'category', 'tournament_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'category': forms.Select(choices=[(k, v) for k, v in CATEGORIES]),
            'tournament_type': forms.Select(choices=[(k, v) for k, v in TOURNAMENT_TYPES])
        }


# Create your views here.

class TournamentView(TemplateView):
    template_name = "tournament/tournament_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournaments'] = Tournament.objects.all()
        context['form'] = TournamentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tournaments')
        return self.render_to_response(self.get_context_data(form=form))


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['last_name', 'first_name', 'points']


class CasuPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['last_name', 'first_name']


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "tournament/tournament_detail.html"
    context_object_name = 'tournament'

    def get_available_players(self):
        print(self.object.category)
        if self.object.category == "C":
            return Player.objects.exclude(tournaments=self.object).exclude(points=0).all().order_by('last_name')
        else:
            return Player.objects.exclude(tournaments=self.object).filter(points=0).all().order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.object.players.order_by('last_name').all()
        context['form'] = PlayerForm()
        available_players = self.get_available_players()
        context['available_players'] = available_players
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.category == "C":
            form = PlayerForm(request.POST)
        else:
            form = CasuPlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            self.object.players.add(player)
            return redirect('tournament_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


def add_player_to_tournament(request, *args, **kwargs):
    tournament = get_object_or_404(Tournament, id=kwargs.get('pk'))
    player = get_object_or_404(Player, id=kwargs.get("player_id"))
    tournament.players.add(player)
    return redirect('tournament_detail', pk=tournament.pk)


def delete_player_from_tournament(request, *args, **kwargs):
    tournament = get_object_or_404(Tournament, id=kwargs.get('pk'))
    player = get_object_or_404(Player, id=kwargs.get("player_id"))
    tournament.players.remove(player)
    return redirect('tournament_detail', pk=tournament.pk)


def pdf_view(request, *args, **kwargs):
    step = Step.objects.get(pk=kwargs.get('step_pk'))
    step_iteration = kwargs.get('step_iteration')
    steps: list[Step] = get_tournament_steps(step, step_iteration)
    max_players = 2
    for step in steps:
        for pool in step.pools.all():
            if pool.players.count() > max_players:
                max_players = pool.players.count()

    match max_players:
        case 3:
            pools_by_page = 6
        case 4:
            pools_by_page = 4
        case 5:
            pools_by_page = 3
        case 6:
            pools_by_page = 2
        case _:
            pools_by_page = 9
    pools = get_steps_pools(
        steps,
        pools_by_page,
        is_last_step=step_iteration > 2)
    context = {
        'pools': pools
    }
    return render_to_pdf('my_template.html', context)
