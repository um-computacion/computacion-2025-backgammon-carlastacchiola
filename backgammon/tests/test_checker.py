import unittest
from backgammon.core.checker import Checker


class TestChecker(unittest.TestCase):

    # --------------------------
    # Inicialización
    # --------------------------
    def test_init_valid(self):
        c = Checker("blanco", 5)
        self.assertEqual(c.get_color(), "blanco")
        self.assertEqual(c.get_position(), 5)
        self.assertFalse(c.is_captured())
        self.assertFalse(c.is_borne_off())

    def test_init_without_position(self):
        c = Checker("negro")
        self.assertEqual(c.get_position(), None)
        self.assertFalse(c.is_captured())
        self.assertFalse(c.is_borne_off())

    def test_init_invalid_color(self):
        with self.assertRaises(TypeError):
            Checker(123)

    def test_init_invalid_position_type(self):
        with self.assertRaises(TypeError):
            Checker("blanco", "no-numero")

    def test_init_invalid_position_range(self):
        with self.assertRaises(ValueError):
            Checker("blanco", 30)

    # --------------------------
    # Movimiento de fichas
    # --------------------------
    def test_move_to_valid(self):
        c = Checker("blanco", 6)
        c.move_to(8)
        self.assertEqual(c.get_position(), 8)

    def test_move_to_invalid_type(self):
        c = Checker("blanco", 5)
        with self.assertRaises(TypeError):
            c.move_to("nueve")

    def test_move_to_invalid_range(self):
        c = Checker("blanco", 5)
        with self.assertRaises(ValueError):
            c.move_to(25)

    def test_move_to_captured(self):
        c = Checker("blanco", 3)
        c.capture()
        with self.assertRaises(ValueError):
            c.move_to(5)

    def test_move_to_borne_off(self):
        c = Checker("blanco", 4)
        c.bear_off()
        with self.assertRaises(ValueError):
            c.move_to(10)

    # --------------------------
    # Captura y reingreso
    # --------------------------
    def test_capture(self):
        c = Checker("negro", 10)
        c.capture()
        self.assertTrue(c.is_captured())
        self.assertEqual(c.get_position(), None)

    def test_reenter_valid(self):
        c = Checker("blanco", 7)
        c.capture()
        c.reenter(3)
        self.assertFalse(c.is_captured())
        self.assertEqual(c.get_position(), 3)

    def test_reenter_not_captured(self):
        c = Checker("blanco", 12)
        with self.assertRaises(ValueError):
            c.reenter(4)

    def test_reenter_invalid_position(self):
        c = Checker("blanco", 2)
        c.capture()
        with self.assertRaises(ValueError):
            c.reenter(0)

    # --------------------------
    # Bearing off
    # --------------------------
    def test_bear_off(self):
        c = Checker("blanco", 24)
        c.bear_off()
        self.assertTrue(c.is_borne_off())
        self.assertEqual(c.get_position(), None)

    # --------------------------
    # Representación en texto
    # --------------------------
    def test_str_on_board(self):
        c = Checker("blanco", 8)
        texto = str(c)
        self.assertIn("Ficha blanco", texto)
        self.assertIn("en la posición 8", texto)

    def test_str_captured(self):
        c = Checker("blanco", 8)
        c.capture()
        self.assertIn("capturada", str(c))

    def test_str_borne_off(self):
        c = Checker("blanco", 15)
        c.bear_off()
        self.assertIn("retirada del tablero", str(c))


if __name__ == "__main__":
    unittest.main()
