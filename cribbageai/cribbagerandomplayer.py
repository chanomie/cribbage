"""This player is random and makes no choices of selection
"""

import random

HIGHEST_RUN_ALLOWED = 31

class RandomPlayer:
    def discard_to_crib(self, player_hand, crib):
        card = random.sample(player_hand, 1)[0]
        player_hand.remove(card)
        crib.add(card)
        card = random.sample(player_hand, 1)[0]
        player_hand.remove(card)
        crib.add(card)

    def get_run_card(self, player_run_hand, run, run_total):
        for card in player_run_hand:
            if run_total + card.value <= HIGHEST_RUN_ALLOWED:
                return card
        