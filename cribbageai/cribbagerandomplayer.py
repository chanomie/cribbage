"""This player is random and makes no choices of selection
"""

import random

HIGHEST_RUN_ALLOWED = 31

class RandomPlayer:
    """Provides a base implementation for a player that makes random choices.
    """
    def discard_to_crib(self, player_hand):
        """Discards two cards randomly to the crib.

        Args:
            player_hand: A set of PlayingCard representing the hand

        Returns:
           {PlayingCard, PlayingCard} two cards as a tuple
        """

        card_one = random.sample(sorted(player_hand), 1)[0]
        player_hand.remove(card_one)
        card_two = random.sample(sorted(player_hand), 1)[0]
        player_hand.remove(card_two)

        return card_one, card_two

    # pylint: disable=unused-argument
    def get_run_card(self, player_run_hand, run, run_total):
        """Selects a random valid card for the run

        Args:
            player_run_hand: The set of PlayingCards the player has in
              their hand available to play.
            run: the existing list of PlayingCards in the run
            run_total: the total value in the run
        """
        for card in player_run_hand:
            if run_total + card.value <= HIGHEST_RUN_ALLOWED:
                return card

        return None
    # pylint: enable=unused-argument
