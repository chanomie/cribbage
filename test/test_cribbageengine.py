import unittest
from cribbageai import cribbageengine

# python3 -m unittest test.test_cribbageengine 
class TestCribbageEngine(unittest.TestCase):
    def test_score_fifteen(self):
        run = [cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.FIVE, 5)]
        run_card = cribbageengine.PlayingCard(cribbageengine.Suit.CLUB, cribbageengine.Face.TEN, 10)
        
        self.assertEqual(cribbageengine.calculate_score_for_run_play(run, run_card), 2)
if __name__ == '__main__':
    unittest.main()