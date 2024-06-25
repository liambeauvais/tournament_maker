from typing import Type

from django.db.models import QuerySet

from game.models import Game
from game_set.models import Set
from player.models import Player
from pool.models import Pool, PoolPLayer


def generate_round_robin_games(players: QuerySet[PoolPLayer], tournament_id: Type[int]):
    num_players = len(players)
    mock_player = Player.objects.get(last_name="Test")

    players_id = [player.player_id for player in players]
    if num_players % 2 != 0:
        players_id.append(mock_player.pk)
        num_players += 1

    players = Player.objects.filter(pk__in=players_id).order_by("points").all()
    # Fix the first player
    fixed_player = players[0]
    rotating_players = players[1:]

    games: list[Game] = []

    for round_num in range(num_players - 1):
        # Add matches for the current round
        games.append(
            Game(
                player_one_id=fixed_player.pk,
                player_two_id=rotating_players[len(rotating_players)-1].pk,
                tournament_id=tournament_id
            )
        )
        for i in range((num_players - 1) // 2):
            games.append(
                Game(
                    player_one_id=rotating_players[i].pk,
                    player_two_id=rotating_players[len(rotating_players) -2 - i].pk,
                    tournament_id=tournament_id
                )
            )

        # Rotate players for the next round
        rotating_players = [rotating_players[len(rotating_players)-1]] + rotating_players[:len(rotating_players)-1]

    games_without_mock = []
    for game in games:
        if game.player_one.pk != mock_player.pk and game.player_two.pk != mock_player.pk:
            games_without_mock.append(game)


    if len(games_without_mock) == 3:
        first_game = games_without_mock.pop(0)
        games_without_mock.append(first_game)
        second_game = games_without_mock.pop(1)
        games_without_mock.insert(0, second_game)

    return games_without_mock


def generate_pool_matches(pools: list[Pool]):
    number_of_sets = pools[0].step.tournament.set_number
    for pool in pools:
        games = generate_round_robin_games(pool.players.all(), pool.step.tournament_id)
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


def generate_pools(numbers_of_pools: int, players: list[Player], step_id: int, players_by_pool: int = None):
    for i in range(numbers_of_pools):
        pool = Pool.objects.create(
            step_id=step_id
        )
        pool.save()
    pools = Pool.objects.filter(step_id=step_id).all()
    count = 0

    for i in range(players_by_pool):
        for pool in pools:
            if len(players) > count:
                pool_player = PoolPLayer.objects.create(
                    pool_id=pool.pk,
                    player_id=players[count].pk
                )
                pool_player.save()
                count += 1
        pools = pools[::-1]

    generate_pool_matches(pools)
