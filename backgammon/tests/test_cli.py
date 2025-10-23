import unittest
from unittest.mock import patch
from backgammon.cli.cli import decide_first_player


class TestFirstPlayerDecision(unittest.TestCase):

    @patch("backgammon.core.dice.random.randint", side_effect=[6, 3])
    def test_player1_wins(self, mock_randint):
        winner, values = decide_first_player()
        self.assertEqual(winner, "Jugador 1")
        self.assertEqual(values, [6, 3])

    @patch("backgammon.core.dice.random.randint", side_effect=[2, 5])
    def test_player2_wins(self, mock_randint):
        winner, values = decide_first_player()
        self.assertEqual(winner, "Jugador 2")
        self.assertEqual(values, [2, 5])

    @patch("backgammon.core.dice.random.randint", side_effect=[4, 4])
    def test_tie(self, mock_randint):
        winner, values = decide_first_player()
        self.assertEqual(winner, "Empate")
        self.assertEqual(values, [4, 4])
