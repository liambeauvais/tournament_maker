from django.db.models.signals import post_save
from django.dispatch import receiver

from game_set.models import Set


@receiver(post_save, sender=Set)
def set_updated(sender, instance: Set, created, **kwargs):
    if not created:
        game = instance.game
        number_of_sets = game.tournament.set_number // 2 + 1
        player_one = 0
        player_two = 0
        for set in game.sets.all():
            if set.score is not None:
                if set.score >= 0:
                    player_one += 1
                else:
                    player_two += 1
        if player_one == number_of_sets or player_two == number_of_sets:
            if player_one == number_of_sets:
                game.winner = game.player_one
                print(game.winner)
            else:
                game.winner = game.player_two
                print(game.winner)
            game.save()
