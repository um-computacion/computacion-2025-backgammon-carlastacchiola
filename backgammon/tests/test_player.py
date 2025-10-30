# backgammon/tests/test_player.py
import unittest
from backgammon.core.player import Player, WHITE, BLACK
from backgammon.core.checker import Checker


class TestPlayer(unittest.TestCase):

    # --------------------------------------------------
    # 1. Inicialización
    # --------------------------------------------------
    def test_initial_state_white_and_black(self):
        """Verifica nombre, color, cantidad de fichas y representación."""
        for color, label in [(WHITE, "Blanco"), (BLACK, "Negro")]:
            with self.subTest(color=color):
                p = Player("Jugador", color)
                self.assertEqual(p.name, "Jugador")
                self.assertEqual(p.color, color)
                self.assertEqual(len(p.checkers), 15)
                self.assertTrue(all(isinstance(c, Checker) for c in p.checkers))
                self.assertIn(label, repr(p))
                self.assertEqual(p.checkers_off, 0)
                self.assertEqual(p.on_bar, 0)

    # --------------------------------------------------
    # 2. Conteos dinámicos
    # --------------------------------------------------
    def test_borne_off_count(self):
        p = Player("Carla", WHITE)
        for i in range(3):
            p.checkers[i].borne_off = True
        self.assertEqual(p.borne_off_count(), 3)

    def test_bar_count(self):
        p = Player("Carla", WHITE)
        p.checkers[0].on_bar = True
        p.checkers[1].on_bar = True
        self.assertEqual(p.bar_count(), 2)

    def test_active_checkers_excludes_borne_off(self):
        p = Player("Carla", WHITE)
        for i in range(5):
            p.checkers[i].borne_off = True
        actives = p.active_checkers()
        self.assertEqual(len(actives), 10)
        self.assertTrue(all(not c.borne_off for c in actives))

    # --------------------------------------------------
    # 3. Reset
    # --------------------------------------------------
    def test_reset_restores_default_state(self):
        """Reset deja todo limpio: sin posiciones, sin barra, sin borne_off."""
        p = Player("Carla", WHITE)
        p.checkers_off = 3
        p.on_bar = 2
        p.checkers[0].borne_off = True
        p.checkers[1].on_bar = True
        p.checkers[2].position = 12

        p.reset()

        self.assertEqual(p.checkers_off, 0)
        self.assertEqual(p.on_bar, 0)
        for c in p.checkers:
            self.assertIsNone(c.position)
            self.assertFalse(c.on_bar)
            self.assertFalse(c.borne_off)

    def test_reset_can_be_called_multiple_times(self):
        """Reset es idempotente: llamarlo varias veces no cambia el resultado."""
        p = Player("Carla", BLACK)
        for i in range(2):
            p.checkers[i].on_bar = True
        p.reset()
        p.reset()
        self.assertEqual(p.bar_count(), 0)
        self.assertEqual(p.borne_off_count(), 0)
        self.assertEqual(len(p.active_checkers()), 15)

    # --------------------------------------------------
    # 4. Representación
    # --------------------------------------------------
    def test_repr_output(self):
        p1 = Player("Carla", WHITE)
        p2 = Player("Pepe", BLACK)
        self.assertEqual(repr(p1), "Player(Carla, Blanco)")
        self.assertEqual(repr(p2), "Player(Pepe, Negro)")


if __name__ == "__main__":
    unittest.main()
