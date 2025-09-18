import unittest
from backgammon.core.player import player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = player("Carla", "blanco")

    def test_inicializacion(self):
        self.assertEqual(self.player.get_name(), "Carla")
        self.assertEqual(self.player.get_color(), "blanco")
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)

    def test_capture_checker(self):
        self.player.capture_checker()
        self.assertEqual(self.player.get_checkers(), 14)
        self.assertEqual(self.player.get_captured(), 1)

    def test_capture_checker_no_negativo(self):
        for _ in range(15):
            self.player.capture_checker()
        self.player.capture_checker() 
        self.assertEqual(self.player.get_checkers(), 0)
        self.assertEqual(self.player.get_captured(), 15)

    def test_reenter_checker(self):
        self.player.capture_checker()
        self.player.reenter_checker()
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)

    def test_reenter_checker_no_negativo(self):
        self.player.reenter_checker() 
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)


    def test_str(self):
        texto = str(self.player)
        self.assertIn("Jugador Carla", texto)
        self.assertIn("blanco", texto)
        self.assertIn("Fichas: 15", texto)
        self.assertIn("Capturadas: 0", texto)


if __name__ == "__main__":
    unittest.main()