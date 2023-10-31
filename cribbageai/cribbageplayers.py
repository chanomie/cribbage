"""This player is random and makes no choices of selection
"""

import logging
import random
from itertools import combinations

import cribbageengine

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

class OptimizedPlayer(RandomPlayer):
    """Provides a run optimized player"""
    def get_run_card(self, player_run_hand, run, run_total):
        """Selects a random valid card for the run

        Args:
            player_run_hand: The set of PlayingCards the player has in
              their hand available to play.
            run: the existing list of PlayingCards in the run
            run_total: the total value in the run
        """
        best_card = None
        best_points = None

        # First see if points can be earned, and maximize that.
        for run_card in player_run_hand:
            if run_total + run_card.value <= HIGHEST_RUN_ALLOWED:
                this_points = cribbageengine.calculate_score_for_run_play(run, run_card)
                logging.debug("OptimizedPlayer Initial Review Card %s for Score %s", run_card, this_points)

                # keep the total under 5 is good
                # as is avoiding leaving a 5 or 10 run total where the opponent
                #   could try and get 15
                if run_total + run_card.value < 5:
                    this_points += 0.5
                elif run_total + run_card.value == 5:
                    this_points -= 0.5
                elif run_total + run_card.value == 15:
                    this_points -= 0.3

                # if the run total is less than 15, and the card takes it above
                # 15 that helps to prevent opponent from getting a 15
                if run_total < 15 < run_total + run_card.value:
                    this_points += 0.5

                logging.debug("OptimizedPlayer Review Card %s for Score %s", run_card, this_points)
                # Choose the card that gives the best points.  If there is a tie
                # choose the largest card we can drop
                if best_points is None or this_points > best_points:
                    best_card = run_card
                    best_points = this_points
                elif this_points == best_points and run_card.value > best_card.value:
                    best_card = run_card
                    best_points = this_points

        logging.info("OptimizedPlayer Best Card %s for Score %s", best_card, best_points)
        return best_card

    def discard_to_crib(self, player_hand):
        """Discards two cards randomly to the crib.

        Args:
            player_hand: A set of PlayingCard representing the hand

        Returns:
           {PlayingCard, PlayingCard} two cards as a tuple
        """

        # Get a deck of all potential cards not included in the hand
        remaining_deck = cribbageengine.CribbageEngine().get_deck_copy()
        for card in player_hand:
            remaining_deck.remove(card)

        logging.debug("Remaining Deck [%s]",
          cribbageengine.cards_as_string(remaining_deck))

        # Go through all combinations of discarding two cards
        best_discard_score = 0
        card_one = None
        card_two = None
        combinations_set = list(combinations(player_hand, 2))
        for combo in combinations_set:
            player_hand_copy = player_hand.copy()
            player_discard = set()
            for discard_card in combo:
              player_hand_copy.remove(discard_card)
              player_discard.add(discard_card)

            logging.debug("Calculate Hand Value For: %s",
              cribbageengine.cards_as_string(player_hand_copy))
            logging.debug("Calculate Crib Value For: %s",
              cribbageengine.cards_as_string(player_discard))
            average_score = self._calculate_average_hand_score(player_hand_copy, remaining_deck)

            if average_score > best_discard_score or card_one is None:
              card_one = combo[0]
              card_two = combo[1]
              best_discard_score = average_score

        logging.info("Discard best option [%s] with score [%s]",
          cribbageengine.cards_as_string([card_one,card_two]), best_discard_score)
        player_hand.remove(card_one)
        player_hand.remove(card_two)

        return card_one, card_two

    def _calculate_average_hand_score(self, player_hand, remaining_deck):
        iteration = 0
        total_score = 0
        for run_card in remaining_deck:
            iteration += 1
            total_hand_score = cribbageengine.calculate_score_for_hand(list(player_hand), run_card)

            total_score += total_hand_score

        logging.info("Total Iterations %s has total score %s (%s)", iteration,
          total_score, total_score / iteration)

        return total_score / iteration
