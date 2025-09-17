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
