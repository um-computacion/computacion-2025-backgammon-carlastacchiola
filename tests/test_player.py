# backgammon/tests/test_player.py
import unittest
from core.player import Player, WHITE, BLACK
from core.checker import Checker


class TestPlayer(unittest.TestCase):

    # --------------------------------------------------
    # 1. Inicialización
    # --------------------------------------------------
    def test_initial_state_white_and_black(self):
        """Verifica nombre, color, cantidad de fichas y representación."""
        for color, label in [(WHITE, "Blanco"), (BLACK, "Negro")]:
            with self.subTest(color=color):
                p = Player("Jugador", color)
                self.assertEqual(p.__name__, "Jugador")
                self.assertEqual(p.__color__, color)
                self.assertEqual(len(p.__checkers__), 15)
                self.assertTrue(all(isinstance(c, Checker) for c in p.__checkers__))
                self.assertIn(label, repr(p))
                self.assertEqual(p.__checkers_off__, 0)
                self.assertEqual(p.__on_bar__, 0)
                rep = repr(p)
                self.assertIn(label, rep)
                self.assertIn("Jugador", rep)

    # --------------------------------------------------
    # 2. Conteos dinámicos
    # --------------------------------------------------
    def test_borne_off_count(self):
        """Verifica que borne_off_count() cuente solo las fichas retiradas."""
        p = Player("Carla", WHITE)
        for i in range(3):
            p.__checkers__[i].__borne_off__ = True
        self.assertEqual(p.borne_off_count(), 3)
        p.__checkers__[5].__on_bar__ = True
        self.assertEqual(p.borne_off_count(), 3)

    def test_bar_count_returns_only_checkers_on_bar(self):
        """Cuenta correctamente las fichas que están en la barra."""
        p = Player("Carla", WHITE)
        for c in p.__checkers__:
            c.__on_bar__ = False
            c.__borne_off__ = False
        p.__checkers__[0].__on_bar__ = True
        p.__checkers__[1].__on_bar__ = True
        p.__checkers__[2].__borne_off__ = True
        p.__checkers__[2].__on_bar__ = False
        self.assertEqual(p.bar_count(), 2)

    def test_active_checkers_excludes_borne_off(self):
        p = Player("Carla", WHITE)
        for i in range(5):
            p.__checkers__[i].__borne_off__ = True
        actives = p.active_checkers()
        self.assertEqual(len(actives), 10)
        self.assertTrue(all(not c.__borne_off__ for c in actives))

    # --------------------------------------------------
    # 3. Reset
    # --------------------------------------------------
    
    def test_reset_restores_default_state(self):
        """
        Reset deja todo limpio: sin posiciones, sin barra, sin borne_off
        ni fichas fuera del tablero.
        """
        p = Player("Carla", WHITE)
        # Alteramos algunos valores
        p.__checkers_off__ = 3
        p.__on_bar__ = 2
        p.__checkers__[0].__borne_off__ = True
        p.__checkers__[1].__on_bar__ = True
        p.__checkers__[2].__position__ = 12

        p.reset()

        self.assertEqual(p.__checkers_off__, 0)
        self.assertEqual(p.__on_bar__, 0)
        # Todas las fichas deben volver al estado neutro
        for c in p.__checkers__:
            self.assertIsNone(c.__position__)
            self.assertFalse(c.__on_bar__)
            self.assertFalse(c.__borne_off__)
        

    def test_reset_can_be_called_multiple_times(self):
        """Reset es idempotente: llamarlo varias veces no cambia el resultado."""
        p = Player("Carla", BLACK)
        for i in range(2):
            p.__checkers__[i].__on_bar__ = True
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