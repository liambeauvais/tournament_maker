from typing import Type

from django.db.models import QuerySet

from game.models import Game
from game_set.models import Set
from player.models import Player
from pool.models import Pool, PoolPLayer


def generate_round_robin_games(pool_players: QuerySet[PoolPLayer], tournament_id: Type[int]):
    num_players = len(pool_players)
    mock_player = Player.objects.get(last_name="Test")

    players = [pool_player.player for pool_player in pool_players]
    if num_players % 2 != 0:
        players.append(mock_player)
        num_players += 1

    players_indexed = [
        {'index': index, 'player': players[index]}
        for index in range(num_players)
    ]
    # Fix the first player
    fixed_player = players_indexed[0]
    rotating_players = players_indexed[1:]
    games: list[Game] = []

    for round_num in range(num_players - 1):
        # Add matches for the current round
        games.append(
            Game(
                player_one_id=fixed_player['player'].pk,
                player_two_id=rotating_players[len(rotating_players) - 1]['player'].pk,
                tournament_id=tournament_id
            )
        )
        for i in range((num_players - 1) // 2):
            opponents = [
                rotating_players[i],
                rotating_players[len(rotating_players) - 2 - i],
            ]
            opponents = sorted(opponents, key=lambda x: x['index'])
            games.append(
                Game(
                    player_one_id=opponents[0]['player'].pk,
                    player_two_id=opponents[1]['player'].pk,
                    tournament_id=tournament_id
                )
            )

        # Rotate players for the next round
        rotating_players = [rotating_players[len(rotating_players) - 1]] + rotating_players[:len(rotating_players) - 1]

    games_without_mock = []
    for game in games:
        if game.player_one.pk != mock_player.pk and game.player_two.pk != mock_player.pk:
            games_without_mock.append(game)

    if len(games_without_mock) == 3:
        first_game = games_without_mock.pop(0)
        games_without_mock.append(first_game)
    return games_without_mock


def generate_pool_matches(pools: list[Pool]):
    number_of_sets = pools[0].step.set_number
    for pool in pools:
        games = generate_round_robin_games(pool.players.all(), pool.step.tournament_id)
        games = Game.objects.bulk_create(
            games
        )
        for game in games:
            pool.games.add(game)
            pool.save()

            sets = []
            for i in range(number_of_sets):
                sets.append(Set(
                    game_id=game.pk,
                    number=i + 1
                ))
            Set.objects.bulk_create(sets)


def generate_pools(numbers_of_pools: int, players: QuerySet[Player], step_id: int, players_by_pool: int = None):
    pools = [
        Pool(step_id=step_id)
        for _ in range(numbers_of_pools)
    ]
    pools = Pool.objects.bulk_create(pools)

    count = 0
    players_sorted = players.order_by("-points")
    pool_players = []
    for i in range(players_by_pool):
        for pool in pools:
            if len(players) > count:
                pool_players.append(
                    PoolPLayer(
                        pool_id=pool.pk,
                        player_id=players_sorted[count].pk
                    )
                )
                count += 1
        pools = pools[::-1]
    PoolPLayer.objects.bulk_create(pool_players)
    generate_pool_matches(pools)
