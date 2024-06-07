from django.shortcuts import get_object_or_404

from game.models import Game
from game_set.models import Set
from player.models import Player
from pool.models import Pool
from step.models import Step, StepPLayer
from tournament.models import Tournament


def generate_round_robin_games(players: list[Player]):
    num_players = len(players)
    mock_player = Player.objects.get(last_name="Test")
    if num_players % 2 != 0:
        players.append(mock_player)
        num_players += 1
    # Fix the first player
    fixed_player = players[0]
    rotating_players = players[1:]

    games: list[Game] = []

    for round_num in range(num_players - 1):
        # Add matches for the current round
        games.append(
            Game(
                player_one_id=fixed_player.pk,
                player_two_id=rotating_players[-1].pk
            )
        )
        for i in range((num_players - 1) // 2):
            games.append(
                Game(
                    player_one_id=rotating_players[i].pk,
                    player_two_id=rotating_players[-2 - i].pk
                )
            )

        # Rotate players for the next round
        rotating_players = [rotating_players[-1]] + rotating_players[:-1]
    for game in games:
        if game.player_one.pk == mock_player.pk or game.player_two.pk == mock_player.pk:
            del game
    return games


# Create your views here.

def generate_pool_matches(pools: list[Pool]):
    number_of_sets = pools[0].step.tournament.set_number
    for pool in pools:
        games = generate_round_robin_games(pool.players.all())
        games = Game.objects.bulk_create(
            games
        )
        for game in games:
            pool.games.add(game)
            pool.save()

            for i in range(number_of_sets):
                set = Set.objects.create(
                    game_id=game.pk,
                    number=i + 1
                )
                set.save()


def generate_pools(numbers_of_pools: int, players: list[Player], step_id: int, players_by_pool: int):
    pools = []
    for i in range(numbers_of_pools):
        pool = Pool.objects.create(
            step_id=step_id
        )
        pool.save()
        pools.append(pool)
    for i in range(players_by_pool):
        for pool in pools:
            if len(players) > 0:
                pool.players.add(players.pop(0))
                pool.save()
        pools = pools.reverse()

    generate_pool_matches(pools)


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

        numbers_of_pools = (len(players) // 3 +
                            (3 - (len(players) % 3)) if len(players) % 3 != 0
                            else 0
                            )

        generate_pools(numbers_of_pools, players, step.pk, 3)
