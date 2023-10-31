"""
Unit testing class for the the CribbageEngine
"""

import logging
import os
import sys
import unittest

# This seems like a hack, but I couldn't figure out how to avoid ModuleNotFound
sys.path.append(os.getcwd() + "/cribbageai")
from cribbageai.cribbageplayers import OptimizedPlayer
from cribbageai.cribbageengine import CribbageGame
from cribbageai.cribbageengine import PlayingCard
from cribbageai.cribbageengine import Face
from cribbageai.cribbageengine import Suit

class TestCribbagePlayers(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename='cribbageapp.log', level=logging.DEBUG,
          format='%(asctime)s - %(levelname)s - %(message)s')

    def test_run_selection_stay_under_five(self):
        player = OptimizedPlayer()

        expected_card = PlayingCard(Suit.CLUB, Face.FOUR, 4)

        run = [PlayingCard(Suit.CLUB, Face.TWO, 2)]
        run_total = CribbageGame.get_cards_total_value(run)
        player_run_hand = [PlayingCard(Suit.CLUB, Face.THREE, 3),
          expected_card]

        selected_card = player.get_run_card(player_run_hand, run, run_total)

        self.assertEqual(expected_card, selected_card)

if __name__ == '__main__':
    unittest.main()