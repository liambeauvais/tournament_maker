from django import forms
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView

from player.models import Player
from .models import Tournament, TYPES


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['date', 'name', 'set_number', 'type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'type': forms.Select(choices=[(k, v) for k, v in TYPES])
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
            if self.object.type == "C":
                return Player.objects.exclude(tournaments=self.object).exclude(points=0)
            else:
                return Player.objects.exclude(tournaments=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.object.players.order_by('last_name').all()
        context['form'] = PlayerForm()
        available_players = self.get_available_players()
        context['available_players'] = available_players
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object.type)
        if self.object.type == "C":
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



