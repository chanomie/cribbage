import unittest
from cribbageai import cribbageengine

# python3 -m unittest test.test_cribbageengine 
class TestCribbageEngine(unittest.TestCase):
    def test_run_score_fifteen(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.FIVE, 5)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.TEN, 10)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)

    def test_run_score_fifteen(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.THREE, 3),
        cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.TWO, 2)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.TEN, 10)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)


    def test_run_score_thirtyone(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.TEN, 10),
          cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.EIGHT, 8),
          cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.FIVE, 5)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.EIGHT, 8)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)

    def test_run_score_pair(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.FIVE, 5)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.SPADE, cribbageengine.Face.FIVE, 5)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)

    def test_run_score_triple(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.TWO, 2),
          cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.TWO, 2)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.SPADE, cribbageengine.Face.TWO, 2)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 6)

    def test_run_score_quadruple(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.FIVE, 5),
          cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.FIVE, 5),
          cribbageengine.PlayingCard(cribbageengine.Suit.HEART, cribbageengine.Face.FIVE, 5)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.SPADE, cribbageengine.Face.FIVE, 5)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 12)

    def test_run_score_sequence_three(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.FIVE, 5),
          cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.SIX, 6)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.SPADE, cribbageengine.Face.SEVEN, 7)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 3)

    def test_run_score_sequence_three_out_of_order(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.FIVE, 5),
          cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.SEVEN, 7)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.SPADE, cribbageengine.Face.SIX, 6)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 3)

    def test_run_score_sequence_four_out_of_order(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.FIVE, 5),
          cribbageengine.PlayingCard(cribbageengine.Suit.DIAMOND, cribbageengine.Face.SEVEN, 7),
          cribbageengine.PlayingCard(cribbageengine.Suit.SPADE, cribbageengine.Face.SIX, 6)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.SPADE, cribbageengine.Face.FOUR, 4)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 4)
        
        
if __name__ == '__main__':
    unittest.main()