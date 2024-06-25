from pool.models import Pool


def get_results(pool_games, results, type: str):
    for game in pool_games:
        for game_set in game.sets.all():
            if game_set.score is not None:
                if type == "points":
                    game_score = abs(game_set.score)
                    winner_points = 11 if game_score < 9 else game_score + 2
                    loser_points = game_score
                else:
                    winner_points = 1
                    loser_points = 0

                if game_set.score > 0:
                    results[game.player_one.pk]["won"] += winner_points
                    results[game.player_one.pk]["lost"] += loser_points
                    results[game.player_two.pk]["won"] += loser_points
                    results[game.player_two.pk]["lost"] += winner_points
                else:
                    results[game.player_one.pk]["won"] += loser_points
                    results[game.player_one.pk]["lost"] += winner_points
                    results[game.player_two.pk]["won"] += winner_points
                    results[game.player_two.pk]["lost"] += loser_points
    return results


def create_pool_scoreboard(pool: Pool):
    pool_games = pool.games.all()
    results = {
        pool_player.player_id: {"won": 0, "lost": 0}
        for pool_player in pool.players.all()
    }
    for game in pool_games:
        results[game.winner.pk]["won"] += 1
    coeffs = {
        player_pk: round(scores["won"] / scores["lost"] if scores["lost"] != 0 else scores["won"], 2)
        for player_pk, scores in results.items()
    }

    # if equality on games
    if len(set(coeffs.values())) != len(coeffs):
        results = get_results(pool_games, results, "sets")
        coeffs = {
            player_pk: round(scores["won"] / scores["lost"] if scores["lost"] != 0 else scores["won"], 2)
            for player_pk, scores in results.items()
        }

    # equality on sets
    if len(set(coeffs.values())) != len(coeffs):
        results = get_results(pool_games, results, "points")
        coeffs = {
            player_pk: round(scores["won"] / scores["lost"], 2)
            for player_pk, scores in results.items()
        }

    return [
        {"player_pk": player_pk, "coeff": coeff}
        for player_pk, coeff in coeffs.items()
    ]
