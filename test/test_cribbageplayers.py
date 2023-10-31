"""
Unit testing class for the the CribbageEngine
"""

import logging
import os
import sys
import unittest

# This seems like a hack, but I couldn't figure out how to avoid ModuleNotFound
sys.path.append(os.getcwd() + "/cribbageai")
from cribbageplayers import OptimizedPlayer
from cribbageengine import CribbageEngine
from cribbageengine import CribbageGame
from cribbageengine import PlayingCard
from cribbageengine import Face
from cribbageengine import Suit

class TestCribbagePlayers(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename='cribbageapp.log', level=logging.DEBUG,
          format='%(asctime)s - %(levelname)s - %(message)s')

    def test_playing_card_equals(self):
        self.assertEqual(PlayingCard(Suit.CLUB, Face.TWO, 2),PlayingCard(Suit.CLUB, Face.TWO, 2))

    def test_playing_card_contains(self):
        deck_of_cards = CribbageEngine().get_deck_copy()
        single_card = PlayingCard(Suit.CLUB, Face.TWO, 2)

        self.assertTrue(single_card in deck_of_cards)

    def test_run_selection_stay_under_five(self):
        player = OptimizedPlayer()

        expected_card = PlayingCard(Suit.CLUB, Face.FOUR, 4)

        run = [PlayingCard(Suit.CLUB, Face.TWO, 2)]
        run_total = CribbageGame.get_cards_total_value(run)
        player_run_hand = [PlayingCard(Suit.CLUB, Face.THREE, 3),
          expected_card]

        selected_card = player.get_run_card(player_run_hand, run, run_total)

        self.assertEqual(expected_card, selected_card)

    def test_discard_to_crib(self):
        player = OptimizedPlayer()
        player_hand = [
          PlayingCard(Suit.SPADE, Face.KING, 10),
          PlayingCard(Suit.HEART, Face.KING, 10),
          PlayingCard(Suit.DIAMOND, Face.KING, 10),
          PlayingCard(Suit.SPADE, Face.FIVE, 5),
          PlayingCard(Suit.DIAMOND, Face.ACE, 1),
          PlayingCard(Suit.HEART, Face.TWO, 2)]

        player.discard_to_crib(player_hand)



if __name__ == '__main__':
    unittest.main()