from pool.models import Pool


class PlayerForSettle:
    def __init__(self, player_id: int, name: str):
        self.id = player_id
        self.name = name
        self.coefficient = 0
        self.wins = 0
        self.won_sets = 0
        self.lost_sets = 0
        self.won_points = 0
        self.lost_points = 0
        self.matches = []

    def __str__(self):
        return f"{self.name}"

    def ratio_sets(self, opponents: list[int]):
        won_sets, lost_sets = 0, 0
        for match in self.matches:
            if match[0] in opponents:
                print()
                won_sets += match[1]
                lost_sets += match[2]
        if self.lost_sets == 0:
            return float('inf')
        return won_sets / lost_sets

    def ratio_points(self, opponents: list[int]):
        won_points, lost_points = 0, 0
        for match in self.matches:
            if match[0] in opponents:
                won_points += match[3]
                lost_points += match[4]
        if self.lost_points == 0:
            return float('inf')
        return won_points / lost_points

    def add_result(self, opponent: int, won_sets, lost_sets, won_points, lost_points):
        self.won_sets += won_sets
        self.lost_sets += lost_sets
        self.won_points += won_points
        self.lost_points += lost_points
        self.matches.append(
            [opponent, won_sets, lost_sets, won_points, lost_points]
        )
        if won_sets > lost_sets:
            self.wins += 1


def calculate_results(pool_games, players: dict[int, PlayerForSettle]):
    for game in pool_games:
        results = {
            "player_one": {
                "sets": 0,
                "points": 0
            },
            "player_two": {
                "sets": 0,
                "points": 0
            }
        }
        player_one = players[game.player_one.id]
        player_two = players[game.player_two.id]
        for game_set in game.sets.all():
            if game_set.score is not None:
                game_score = abs(game_set.score)
                winner_points = 11 if game_score < 9 else game_score + 2
                loser_points = game_score
                if game_set.score >= 0:
                    results["player_one"]["points"] += winner_points
                    results["player_two"]["points"] += loser_points
                    results["player_one"]["sets"] += 1
                else:
                    results["player_one"]["points"] += loser_points
                    results["player_two"]["points"] += winner_points
                    results["player_two"]["sets"] += 1
        player_one.add_result(
            opponent=player_two.id,
            won_sets=results["player_one"]["sets"],
            lost_sets=results["player_two"]["sets"],
            won_points=results["player_one"]["points"],
            lost_points=results["player_two"]["points"]
        )
        player_two.add_result(
            opponent=player_one.id,
            won_sets=results["player_two"]["sets"],
            lost_sets=results["player_one"]["sets"],
            won_points=results["player_two"]["points"],
            lost_points=results["player_one"]["points"]
        )


def create_pool_scoreboard(pool: Pool):
    pool_games = pool.games.all()
    pool_players = pool.players.all()
    players_for_settle: dict[int, PlayerForSettle] = {}
    for pool_player in pool_players:
        players_for_settle[pool_player.player_id] = PlayerForSettle(pool_player.player_id, pool_player.player.last_name)
    calculate_results(pool_games, players_for_settle)

    sorted_players = sorted(
        [player_for_settle for player_id, player_for_settle in players_for_settle.items()],
        key=lambda p: p.wins,
        reverse=True
    )
    groups: dict[int, list[PlayerForSettle]] = {}
    for player in sorted_players:
        if player.wins not in groups:
            groups[player.wins] = []
        groups[player.wins].append(player)

    results = []
    for wins, group in groups.items():
        if len(group) > 1:
            opponents = [opponent.id for opponent in group]
            group = settle_equalities(group=group, opponents=opponents, type="sets")
            set_group = set([player.ratio_sets(opponents) for player in group])
            if len(set_group) == 1:
                group = settle_equalities(group=group, opponents=opponents, type="points")

        else:
            for player_for_settle in group:
                player_for_settle.coefficient = player_for_settle.wins
        results.extend(group)
    return results


def settle_equalities(group: list[PlayerForSettle], opponents: list[int], type: str) -> list[PlayerForSettle]:
    if type == "sets":
        sorted_group = sorted(group, key=lambda p: p.ratio_sets(opponents), reverse=True)
        for player_for_settle in sorted_group:
            player_for_settle.coefficient = round(player_for_settle.ratio_sets(opponents), 2)
    else:
        sorted_group = sorted(group, key=lambda p: p.ratio_points(opponents), reverse=True)
        for player_for_settle in sorted_group:
            player_for_settle.coefficient = round(player_for_settle.ratio_points(opponents), 2)

    return sorted_group
