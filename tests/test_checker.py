import unittest
from core.checker import Checker, WHITE, BLACK


class TestChecker(unittest.TestCase):
    # --------------------------------------------------
    # 1. Inicialización
    # --------------------------------------------------
    def test_initial_state_white_and_black(self):
        c1 = Checker(WHITE)
        c2 = Checker(BLACK)

        self.assertEqual(c1.__color__, WHITE)
        self.assertEqual(c2.__color__, BLACK)

        for c in (c1, c2):
            self.assertIsNone(c.__position__)
            self.assertFalse(c.__on_bar__)
            self.assertFalse(c.__borne_off__)
            self.assertTrue(c.is_active())  # activa aunque sin posición

        self.assertIn("Blanca", repr(c1))
        self.assertIn("Negra", repr(c2))

    # --------------------------------------------------
    # 2. Movimiento normal
    # --------------------------------------------------
    def test_move_to_point_updates_all_states(self):
        c = Checker(WHITE)
        c.move_to_point(10)
        self.assertEqual(c.__position__, 10)
        self.assertFalse(c.__on_bar__)
        self.assertFalse(c.__borne_off__)
        self.assertIn("punto 11", repr(c))
        # mover nuevamente a otro punto
        c.move_to_point(0)
        self.assertIn("punto 1", repr(c))

    # --------------------------------------------------
    # 3. Enviar a la barra
    # --------------------------------------------------
    def test_send_to_bar_from_board_and_reset_position(self):
        c = Checker(WHITE)
        c.move_to_point(5)
        c.send_to_bar()
        self.assertIsNone(c.__position__)
        self.assertTrue(c.__on_bar__)
        self.assertFalse(c.__borne_off__)
        self.assertIn("en barra", repr(c))
        # si la volvemos a enviar a barra, no rompe nada
        c.send_to_bar()
        self.assertTrue(c.__on_bar__)

    # --------------------------------------------------
    # 4. Sacar del tablero (borne off)
    # --------------------------------------------------
    def test_bear_off_from_board_and_repr(self):
        c = Checker(BLACK)
        c.move_to_point(7)
        c.bear_off()
        self.assertTrue(c.__borne_off__)
        self.assertFalse(c.__on_bar__)
        self.assertIsNone(c.__position__)
        self.assertIn("fuera del tablero", repr(c))
        # si la volvemos a sacar, no cambia estado
        c.bear_off()
        self.assertTrue(c.__borne_off__)

    # --------------------------------------------------
    # 5. Transiciones combinadas
    # --------------------------------------------------
    def test_transitions_sequence(self):
        c = Checker(WHITE)
        c.move_to_point(3)
        c.send_to_bar()
        self.assertTrue(c.__on_bar__)
        self.assertFalse(c.__borne_off__)
        c.bear_off()
        self.assertTrue(c.__borne_off__)
        self.assertFalse(c.__on_bar__)
        c.move_to_point(15)
        # volver al tablero debería reactivar
        self.assertFalse(c.__borne_off__)
        self.assertFalse(c.__on_bar__)
        self.assertEqual(c.__position__, 15)

    # --------------------------------------------------
    # 6. is_active en todos los estados
    # --------------------------------------------------
    def test_is_active_behavior(self):
        c = Checker(WHITE)
        # En tablero
        c.move_to_point(2)
        self.assertTrue(c.is_active())
        # En barra
        c.send_to_bar()
        self.assertTrue(c.is_active())
        # Fuera del tablero
        c.bear_off()
        self.assertFalse(c.is_active())


if __name__ == "__main__":
    unittest.main()