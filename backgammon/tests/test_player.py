import unittest
from backgammon.core.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Crea un jugador de ejemplo antes de cada test."""
        self.player = Player(1, "Carla", "blanco")

    # ------------------------------
    # Inicialización y getters
    # ------------------------------
    def test_inicializacion(self):
        self.assertEqual(self.player.get_id(), 1)
        self.assertEqual(self.player.get_name(), "Carla")
        self.assertEqual(self.player.get_color(), "blanco")
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)
        self.assertEqual(self.player.get_borne_off(), 0)
        self.assertEqual(self.player.get_score(), 0)
        self.assertEqual(self.player.get_turns(), 0)
        self.assertEqual(self.player.get_history(), [])

    def test_set_color(self):
        self.player.set_color("negro")
        self.assertEqual(self.player.get_color(), "negro")

    # ------------------------------
    # Puntaje
    # ------------------------------
    def test_add_score(self):
        self.player.add_score(5)
        self.player.add_score(10)
        self.assertEqual(self.player.get_score(), 15)

    # ------------------------------
    # Captura y reingreso de fichas
    # ------------------------------
    def test_capture_checker(self):
        self.player.capture_checker()
        self.assertEqual(self.player.get_checkers(), 14)
        self.assertEqual(self.player.get_captured(), 1)
        self.assertIn("capturó ficha", self.player.get_history()[-1])

    def test_capture_checker_error(self):
        # Dejar sin fichas
        for _ in range(15):
            self.player.capture_checker()
        with self.assertRaises(ValueError):
            self.player.capture_checker()

    def test_reenter_checker(self):
        self.player.capture_checker()
        self.player.reenter_checker()
        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)
        self.assertIn("reingresó ficha", self.player.get_history()[-1])

    def test_reenter_checker_error(self):
        with self.assertRaises(ValueError):
            self.player.reenter_checker()

    # ------------------------------
    # Bear off y victoria
    # ------------------------------
    def test_bear_off_checker(self):
        self.player.bear_off_checker()
        self.assertEqual(self.player.get_checkers(), 14)
        self.assertEqual(self.player.get_borne_off(), 1)
        self.assertIn("sacó ficha del tablero", self.player.get_history()[-1])

    def test_bear_off_checker_error(self):
        for _ in range(15):
            self.player.bear_off_checker()
        with self.assertRaises(ValueError):
            self.player.bear_off_checker()

    def test_has_won(self):
        for _ in range(15):
            self.player.bear_off_checker()
        self.assertTrue(self.player.has_won())

    # ------------------------------
    # Turnos y movimiento
    # ------------------------------
    def test_add_turn(self):
        self.player.add_turn()
        self.assertEqual(self.player.get_turns(), 1)
        self.assertIn("jugó turno #1", self.player.get_history()[-1])

    def test_can_move(self):
        self.assertTrue(self.player.can_move())
        for _ in range(15):
            self.player.bear_off_checker()
        self.assertFalse(self.player.can_move())

    # ------------------------------
    # Reset y resumen
    # ------------------------------
    def test_reset(self):
        self.player.capture_checker()
        self.player.add_score(10)
        self.player.add_turn()
        self.player.bear_off_checker()
        self.player.reset()

        self.assertEqual(self.player.get_checkers(), 15)
        self.assertEqual(self.player.get_captured(), 0)
        self.assertEqual(self.player.get_borne_off(), 0)
        self.assertEqual(self.player.get_score(), 0)
        self.assertEqual(self.player.get_turns(), 0)
        self.assertEqual(self.player.get_history(), [])

    def test_summary(self):
        resumen = self.player.summary()
        self.assertIsInstance(resumen, dict)
        self.assertIn("id", resumen)
        self.assertIn("name", resumen)
        self.assertEqual(resumen["checkers"], 15)

    # ------------------------------
    # Representación en texto
    # ------------------------------
    def test_str(self):
        texto = str(self.player)
        self.assertIn("Jugador Carla", texto)
        self.assertIn("blanco", texto)
        self.assertIn("Fichas: 15", texto)
        self.assertIn("Capturadas: 0", texto)


if __name__ == "__main__":
    unittest.main()
