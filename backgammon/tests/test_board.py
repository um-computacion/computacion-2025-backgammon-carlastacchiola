import unittest
from backgammon.core.board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        """Crea un tablero nuevo antes de cada test."""
        self.board = Board()

    # --------------------------
    # Inicialización
    # --------------------------
    def test_initial_setup(self):
        """Verifica que el tablero se inicialice correctamente."""
        points = self.board.get_all_points()
        self.assertEqual(len(points), 24)
        self.assertEqual(self.board.get_point(1), (2, 1))
        self.assertEqual(self.board.get_point(6), (5, 2))
        self.assertEqual(self.board.get_bar(1), 0)
        self.assertEqual(self.board.get_bar(2), 0)

    def test_get_point_invalid(self):
        """Debe lanzar error si la posición es inválida."""
        with self.assertRaises(ValueError):
            self.board.get_point(0)
        with self.assertRaises(ValueError):
            self.board.get_point(25)

    # --------------------------
    # Barra y borne off
    # --------------------------
    def test_get_bar_invalid_player(self):
        """Debe lanzar error si el ID de jugador no es válido."""
        with self.assertRaises(ValueError):
            self.board.get_bar(3)

    def test_add_to_bar_and_reenter(self):
        """Agrega y quita fichas de la barra correctamente."""
        self.board.add_to_bar(1)
        self.assertEqual(self.board.get_bar(1), 1)
        self.board.reenter_from_bar(1)
        self.assertEqual(self.board.get_bar(1), 0)

    def test_reenter_from_empty_bar(self):
        """Debe lanzar error si se intenta reingresar sin fichas."""
        with self.assertRaises(ValueError):
            self.board.reenter_from_bar(1)

    def test_bear_off_checker(self):
        """Debe incrementar correctamente el borne off."""
        self.board.bear_off_checker(1)
        self.assertEqual(self.board.get_borne_off(1), 1)
        self.board.bear_off_checker(2)
        self.assertEqual(self.board.get_borne_off(2), 1)

    def test_bear_off_invalid_id(self):
        """Debe lanzar error con ID inválido."""
        with self.assertRaises(ValueError):
            self.board.bear_off_checker(99)

    # --------------------------
    # Movimientos
    # --------------------------
    def test_move_checker_to_empty(self):
        """Mueve una ficha a un punto vacío correctamente."""
        self.board.move_checker(1, 2, 1)
        self.assertEqual(self.board.get_point(1), (1, 1))
        self.assertEqual(self.board.get_point(2), (1, 1))

    def test_move_checker_to_same_player(self):
        """Mueve una ficha a un punto con fichas del mismo jugador."""
        # punto 12 tiene 5 fichas del jugador 1
        self.board.move_checker(12, 11, 1)
        count, player = self.board.get_point(11)
        self.assertEqual(player, 1)
        self.assertEqual(count, 1)

    def test_move_checker_invalid_position(self):
        """Debe lanzar error con posiciones inválidas."""
        with self.assertRaises(ValueError):
            self.board.move_checker(0, 10, 1)
        with self.assertRaises(ValueError):
            self.board.move_checker(1, 30, 2)

    def test_move_checker_invalid_player(self):
        """Debe lanzar error con jugador inválido."""
        with self.assertRaises(ValueError):
            self.board.move_checker(1, 2, 3)

    def test_move_checker_no_piece(self):
        """Debe lanzar error si el punto de inicio no tiene fichas del jugador."""
        with self.assertRaises(ValueError):
            self.board.move_checker(2, 3, 1)

    def test_move_checker_capture(self):
        """Debe capturar correctamente una ficha rival solitaria."""
        # Asegurar que el punto 1 tenga una ficha del jugador 1
        self.board._points[1] = (1, 1)
        # Y el punto 2 tenga una ficha rival (una sola)
        self.board._points[2] = (1, 2)

        self.board.move_checker(1, 2, 1)
        self.assertEqual(self.board.get_point(2), (1, 1))
        self.assertEqual(self.board.get_bar(2), 1)

    def test_move_checker_blocked_point(self):
        """Debe lanzar error si el punto destino está bloqueado por el rival."""
        self.board._points[2] = (3, 2)
        with self.assertRaises(ValueError):
            self.board.move_checker(1, 2, 1)

    # --------------------------
    # Carga, historial y reset
    # --------------------------
    def test_load_points_valid(self):
        """Debe cargar correctamente un nuevo estado de tablero."""
        new_points = [(1, 1)] * 24
        self.board.load_points(new_points)
        self.assertEqual(self.board.get_point(5), (1, 1))

    def test_load_points_invalid_length(self):
        """Debe lanzar error si la lista no tiene 24 elementos."""
        with self.assertRaises(ValueError):
            self.board.load_points([(1, 1)] * 10)

    def test_get_history_and_reset(self):
        """Verifica que el historial se registre y el tablero se reinicie."""
        self.board.move_checker(1, 2, 1)
        history = self.board.get_history()
        self.assertEqual(len(history), 1)
        self.board.reset_board()
        self.assertEqual(self.board.get_bar(1), 0)

    # --------------------------
    # Representación de texto
    # --------------------------
    def test_str_contains_points_and_bar(self):
        """El string del tablero debe mostrar puntos, barra y borne off."""
        texto = str(self.board)
        self.assertIn("Punto  1", texto)
        self.assertIn("Barra →", texto)
        self.assertIn("Borne Off", texto)


if __name__ == "__main__":
    unittest.main()
