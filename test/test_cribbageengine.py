"""
Unit testing class for the the CribbageEngine
"""

import unittest
from cribbageai import cribbageengine
from cribbageai.cribbageengine import PlayingCard
from cribbageai.cribbageengine import Face
from cribbageai.cribbageengine import Suit

# python3 -m unittest test.test_cribbageengine
class TestCribbageScoringEngine(unittest.TestCase):
    """
    Unit Tests for various scoring mechanisms in the Cribbage Engine
    """
    def test_run_score_fifteen_two_cards(self):
        """ Tests that combination of two cards (5,10) will score 2 points. """
        run = [PlayingCard(Suit.CLUB, Face.FIVE, 5)]
        run_card = PlayingCard(Suit.CLUB, Face.TEN, 10)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)

    def test_run_score_fifteen_three_cards(self):
        """ Tests that combination of three cards (3,2,10) will score 2 points. """
        run = [PlayingCard(Suit.CLUB, Face.THREE, 3),
        PlayingCard(Suit.CLUB, Face.TWO, 2)]
        run_card = PlayingCard(Suit.CLUB, Face.TEN, 10)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)


    def test_run_score_thirtyone(self):
        """ Tests that run hitting thirty one scores two points """
        run = [PlayingCard(Suit.DIAMOND, Face.TEN, 10),
          PlayingCard(Suit.DIAMOND, Face.EIGHT, 8),
          PlayingCard(Suit.DIAMOND, Face.FIVE, 5)]
        run_card = PlayingCard(Suit.CLUB, Face.EIGHT, 8)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)

    def test_run_score_pair(self):
        """ Tests that run with a pair (5,5) scores 2 points """
        run = [PlayingCard(Suit.CLUB, Face.FIVE, 5)]
        run_card = PlayingCard(Suit.SPADE, Face.FIVE, 5)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)

    def test_run_score_triple(self):
        """ Tests that run with a double pair (2,2,2) scores 6 points """
        run = [PlayingCard(Suit.CLUB, Face.TWO, 2),
          PlayingCard(Suit.DIAMOND, Face.TWO, 2)]
        run_card = PlayingCard(Suit.SPADE, Face.TWO, 2)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 6)

    def test_run_score_quadruple(self):
        """ Tests that run with a triple pair (5,5,5,5) scores 12 points """
        run = [PlayingCard(Suit.CLUB, Face.FIVE, 5),
          PlayingCard(Suit.DIAMOND, Face.FIVE, 5),
          PlayingCard(Suit.HEART, Face.FIVE, 5)]
        run_card = PlayingCard(Suit.SPADE, Face.FIVE, 5)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 12)

    def test_run_score_sequence_three(self):
        """ Tests that run with a sequence (5,6,7) scores 3 points """
        run = [PlayingCard(Suit.CLUB, Face.FIVE, 5),
          PlayingCard(Suit.DIAMOND, Face.SIX, 6)]
        run_card = PlayingCard(Suit.SPADE, Face.SEVEN, 7)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 3)

    def test_run_score_sequence_three_out_of_order(self):
        """ Tests that run with a sequence (5,7,6) scores 3 points """
        run = [PlayingCard(Suit.CLUB, Face.FIVE, 5),
          PlayingCard(Suit.DIAMOND, Face.SEVEN, 7)]
        run_card = PlayingCard(Suit.SPADE, Face.SIX, 6)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 3)

    def test_run_score_sequence_four_out_of_order(self):
        """ Tests that run with a sequence (5,7,6,4) scores 4 points """
        run = [PlayingCard(Suit.CLUB, Face.FIVE, 5),
          PlayingCard(Suit.DIAMOND, Face.SEVEN, 7),
          PlayingCard(Suit.SPADE, Face.SIX, 6)]
        run_card = PlayingCard(Suit.SPADE, Face.FOUR, 4)

        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 4)

    def test_calculate_score_for_hand_fifteen(self):
        """ Tests that hand with a 15 (5,7,10,3,2) scores 2 points """
        hand = [PlayingCard(Suit.CLUB, Face.FIVE, 5),
          PlayingCard(Suit.DIAMOND, Face.SEVEN, 7),
          PlayingCard(Suit.SPADE, Face.TEN, 10),
          PlayingCard(Suit.SPADE, Face.THREE, 3)]
        start_card = PlayingCard(Suit.SPADE, Face.TWO, 2)

        self.assertEqual(cribbageengine.calculate_score_for_hand(hand, start_card), 6)

    def test_calculate_score_for_pair(self):
        """ Tests that hand with a pair (7,7,5,9,2) scores 2 points """
        hand = [PlayingCard(Suit.CLUB, Face.SEVEN, 7),
          PlayingCard(Suit.DIAMOND, Face.SEVEN, 7),
          PlayingCard(Suit.SPADE, Face.FIVE, 5),
          PlayingCard(Suit.SPADE, Face.NINE, 9)]
        start_card = PlayingCard(Suit.SPADE, Face.TWO, 2)

        self.assertEqual(cribbageengine.calculate_score_for_hand(hand, start_card), 2)

    def test_calculate_score_for_triple(self):
        """ Tests that hand with a double pair (7,7,7,9,2) scores 6 points """
        hand = [PlayingCard(Suit.CLUB, Face.SEVEN, 7),
          PlayingCard(Suit.DIAMOND, Face.SEVEN, 7),
          PlayingCard(Suit.SPADE, Face.SEVEN, 7),
          PlayingCard(Suit.SPADE, Face.NINE, 9)]
        start_card = PlayingCard(Suit.SPADE, Face.TWO, 2)

        self.assertEqual(cribbageengine.calculate_score_for_hand(hand, start_card), 6)

    def test_calculate_score_for_his_nob(self):
        """ Tests that his nob (7♣,A♦,J♠,9♠),(2♠) scores 1 points """
        hand = [PlayingCard(Suit.CLUB, Face.SEVEN, 7),
          PlayingCard(Suit.DIAMOND, Face.ACE, 1),
          PlayingCard(Suit.SPADE, Face.JACK, 10),
          PlayingCard(Suit.SPADE, Face.NINE, 9)]
        start_card = PlayingCard(Suit.SPADE, Face.TWO, 2)

        self.assertEqual(cribbageengine.calculate_score_for_hand(hand, start_card), 1)

    def test_calculate_score_for_four_flush(self):
        """ Tests that a flush (7♣,A♣,J♣,9♣),(2♠) scores 4 points """
        hand = [PlayingCard(Suit.CLUB, Face.SEVEN, 7),
          PlayingCard(Suit.CLUB, Face.ACE, 1),
          PlayingCard(Suit.CLUB, Face.JACK, 10),
          PlayingCard(Suit.CLUB, Face.NINE, 9)]
        start_card = PlayingCard(Suit.SPADE, Face.TWO, 2)

        self.assertEqual(cribbageengine.calculate_score_for_hand(hand, start_card), 4)

    def test_calculate_score_for_five_flush(self):
        """ Tests that a flush nob (7♣,A♣,J♣,9♣),(2♣) scores 5 points """
        hand = [PlayingCard(Suit.CLUB, Face.SEVEN, 7),
          PlayingCard(Suit.CLUB, Face.ACE, 1),
          PlayingCard(Suit.CLUB, Face.QUEEN, 10),
          PlayingCard(Suit.CLUB, Face.NINE, 9)]
        start_card = PlayingCard(Suit.CLUB, Face.TWO, 2)

        self.assertEqual(cribbageengine.calculate_score_for_hand(hand, start_card), 5)

    # pylint: disable=W0212
    def test_can_sort_cards_to_sequence_false(self):
        """ Tests internal sequence sorter check """
        hand = [PlayingCard(Suit.CLUB, Face.SEVEN, 7),
          PlayingCard(Suit.CLUB, Face.ACE, 1),
          PlayingCard(Suit.CLUB, Face.QUEEN, 10),
          PlayingCard(Suit.CLUB, Face.NINE, 9)]

        self.assertFalse(cribbageengine._can_sort_cards_to_sequence(hand))

    def test_can_sort_cards_to_sequence_true(self):
        """ Tests internal sequence sorter check """
        hand = [PlayingCard(Suit.CLUB, Face.ACE, 1),
          PlayingCard(Suit.CLUB, Face.TWO, 2),
          PlayingCard(Suit.CLUB, Face.FOUR, 4),
          PlayingCard(Suit.CLUB, Face.THREE, 3)]

        self.assertTrue(cribbageengine._can_sort_cards_to_sequence(hand))

    # pylint: enable=W0212

if __name__ == '__main__':
    unittest.main()
