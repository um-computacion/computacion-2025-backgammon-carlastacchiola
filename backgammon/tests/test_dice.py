import unittest
from core.dice import Dice 

class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice()

    def test_roll_single_in_range(self):
        """El dado simple siempre debe estar entre 1 y 6"""
        for _ in range(100):  
            value = self.dice.roll_single()
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 6)

    def test_roll_two_dice_in_range(self):
        """Los dos dados siempre deben estar entre 1 y 6"""
        for _ in range(100):
            values = self.dice.roll()
            self.assertEqual(len(values), 2)
            for v in values:
                self.assertGreaterEqual(v, 1)
                self.assertLessEqual(v, 6)


    def test_values_stored_correctly(self):
        result = self.dice.roll()
        self.assertEqual(result, self.dice.values)


if __name__ == "__main__":
    unittest.main()
