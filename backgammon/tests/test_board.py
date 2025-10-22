"""
Tests unitarios para la clase Board usando unittest.
Verifica la inicialización, movimientos, capturas, bloqueos y errores esperados.
"""

import unittest
from core.board import Board


class TestBoard(unittest.TestCase):
    """Casos de prueba para la clase Board."""

    def setUp(self):
        """Configura un tablero nuevo antes de cada test."""
        self.board = Board()

    def test_initial_positions(self):
        """Verifica que las posiciones iniciales se cargan correctamente."""
        p1 = self.board.get_point(1)
        p6 = self.board.get_point(6)
        self.assertEqual(p1, (2, 1))
        self.assertEqual(p6, (5, 2))
        self.assertEqual(len(self.board.get_all_points()), 24)

    def test_move_simple(self):
        """Verifica que una ficha se mueve correctamente de un punto a otro vacío."""
        self.board.move_checker(1, 2, 1)
        self.assertEqual(self.board.get_point(1)[0], 1)
        self.assertEqual(self.board.get_point(2), (1, 1))

    def test_move_capture(self):
        """Verifica que se captura una ficha rival cuando hay una sola en destino."""
        # Colocamos una sola ficha del jugador 2 en el punto 4
        self.board.__points__[4] = (1, 2)
        # Colocamos una ficha del jugador 1 en el punto 3
        self.board.__points__[3] = (1, 1)

        self.board.move_checker(3, 4, 1)
        self.assertEqual(self.board.get_point(4), (1, 1))
        self.assertEqual(self.board.get_bar(2), 1)

    def test_blocked_point(self):
        """Verifica que no se pueda mover a un punto bloqueado por el rival."""
        self.board.__points__[5] = (2, 2)
        self.board.__points__[4] = (1, 1)

        with self.assertRaises(ValueError):
            self.board.move_checker(4, 5, 1)

    def test_invalid_positions(self):
        """Verifica que no se puedan usar posiciones fuera de rango."""
        with self.assertRaises(ValueError):
            self.board.move_checker(0, 5, 1)
        with self.assertRaises(ValueError):
            self.board.move_checker(1, 25, 1)

    def test_load_points_and_history(self):
        """Verifica la carga manual del tablero y el historial de movimientos."""
        new_points = [(0, 0)] * 24
        self.board.load_points(new_points)
        self.assertTrue(all(p == (0, 0) for p in self.board.get_all_points()))

        # Reasignamos manualmente una ficha para que haya algo que mover
        self.board.__points__[6] = (5, 2)
        self.board.__points__[5] = (0, 0)

        self.board.move_checker(6, 5, 2)
        hist = self.board.get_history()
        self.assertEqual(len(hist), 1)
        self.assertIsInstance(hist[0], tuple)


if __name__ == "__main__":
    unittest.main()
