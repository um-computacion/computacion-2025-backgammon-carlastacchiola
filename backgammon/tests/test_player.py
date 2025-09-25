import unittest
from backgammon.core.player import player
from backgammon.core.player import player
from math import sqrt

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = player(1, "Carla", "blanco")

    def test_inicializacion(self):
        self.assertEqual(self.player.get_name(), "Carla")
        self.assertEqual(self.player.get_color(), "blanco")
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)
        self.assertEqual(self.player.get_score(), 0)

    def test_score(self):
        self.player.add_score(10)
        self.assertEqual(self.player.get_score(), 10)

    def test_capture_checker(self):
        self.player.capture_checker()
        self.assertEqual(self.player.get_checkers(), 14)
        self.assertEqual(self.player.get_captured(), 1)

    def test_capture_checker_no_negativo(self):
        for _ in range(15):
            self.player.capture_checker()
        self.player.capture_checker()  # no debería bajar de 0
        self.assertEqual(self.player.get_checkers(), 0)
        self.assertEqual(self.player.get_captured(), 15)

    def test_reenter_checker(self):
        self.player.capture_checker()
        self.player.reenter_checker()
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)

    def test_reenter_checker_no_negativo(self):
        self.player.reenter_checker()  # no debería romper nada
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)

    def test_bear_off_checker(self):
        self.player.bear_off_checker()
        self.assertEqual(self.player.get_checkers(), 14)

    def test_has_won(self):
        for _ in range(15):
            self.player.bear_off_checker()
        self.assertTrue(self.player.has_won())

    def test_can_move(self):
        self.assertTrue(self.player.can_move())
        for _ in range(15):
            self.player.bear_off_checker()
        self.assertFalse(self.player.can_move())

    def test_str(self):
        texto = str(self.player)
        self.assertIn("Jugador Carla", texto)
        self.assertIn("blanco", texto)
        self.assertIn("Fichas: 15", texto)
        self.assertIn("Capturadas: 0", texto)


if __name__ == "__main__":
    unittest.main()
