import unittest
from backgammon.core.board import Board, WHITE, BLACK


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    # ----------------------------------------------------------
    # 1. SETUP INICIAL
    # ----------------------------------------------------------
    def test_setup_initial(self):
        # Blancas
        self.assertEqual(self.b.points[23], (WHITE, 2))
        self.assertEqual(self.b.points[12], (WHITE, 5))
        self.assertEqual(self.b.points[7], (WHITE, 3))
        self.assertEqual(self.b.points[5], (WHITE, 5))
        # Negras
        self.assertEqual(self.b.points[0], (BLACK, 2))
        self.assertEqual(self.b.points[11], (BLACK, 5))
        self.assertEqual(self.b.points[16], (BLACK, 3))
        self.assertEqual(self.b.points[18], (BLACK, 5))
        # Barras y borne_off vacíos
        self.assertEqual(self.b.bar[WHITE], 0)
        self.assertEqual(self.b.borne_off[BLACK], 0)

    # ----------------------------------------------------------
    # 2. UTILIDADES
    # ----------------------------------------------------------
    def test_opponent_direction_home_range_dest(self):
        b = self.b
        self.assertEqual(b.opponent(WHITE), BLACK)
        self.assertEqual(b.opponent(BLACK), WHITE)
        self.assertEqual(b.direction(WHITE), -1)
        self.assertEqual(b.direction(BLACK), 1)
        self.assertEqual(list(b.home_range(WHITE)), [0, 1, 2, 3, 4, 5])
        self.assertEqual(list(b.home_range(BLACK)), [18, 19, 20, 21, 22, 23])
        self.assertEqual(b.dest_index(WHITE, 23, 3), 20)
        self.assertEqual(b.dest_index(BLACK, 0, 4), 4)

    # ----------------------------------------------------------
    # 3. BLOQUEOS
    # ----------------------------------------------------------
    def test_point_is_blocked_and_bar_entry(self):
        b = self.b
        self.assertTrue(b.point_is_blocked(WHITE, 11))
        self.assertFalse(b.point_is_blocked(BLACK, 11))
        self.assertFalse(b.point_is_blocked(WHITE, -1))
        self.assertFalse(b.point_is_blocked(WHITE, 50))
        self.assertEqual(b.enter_from_bar_targets(WHITE, 6), [18])
        self.assertEqual(b.enter_from_bar_targets(BLACK, 6), [5])

    # ----------------------------------------------------------
    # 4. BEARING OFF - allowed y distance
    # ----------------------------------------------------------
    def test_bearing_off_allowed_false_initial(self):
        self.assertFalse(self.b.bearing_off_allowed(WHITE))
        self.assertFalse(self.b.bearing_off_allowed(BLACK))

    def test_bearing_off_allowed_true_when_all_home(self):
        b = self.b
        b.points = [(0, 0)] * 24
        for i in range(6):
            b.points[i] = (WHITE, 2)
        b.borne_off[WHITE] = 3
        self.assertTrue(b.bearing_off_allowed(WHITE))
        b.bar[WHITE] = 1
        self.assertFalse(b.bearing_off_allowed(WHITE))

    def test_distance_to_bear_off(self):
        b = self.b
        self.assertEqual(b.distance_to_bear_off(WHITE, 0), 1)
        self.assertEqual(b.distance_to_bear_off(WHITE, 5), 6)
        self.assertEqual(b.distance_to_bear_off(BLACK, 23), 1)
        self.assertEqual(b.distance_to_bear_off(BLACK, 18), 6)

    # ----------------------------------------------------------
    # 5. CAN BEAR OFF
    # ----------------------------------------------------------
    def test_can_bear_off_true_only_if_all_home(self):
        b = self.b
        b.points = [(0, 0)] * 24
        # Negras: su casa está en 0–5
        for i in range(0, 6):
            b.points[i] = (BLACK, 2)
        self.assertTrue(b.can_bear_off(BLACK))
        # Si una está fuera de la casa → False
        b.points[10] = (BLACK, 1)
        self.assertFalse(b.can_bear_off(BLACK))


    def test_can_bear_off_with_die(self):
        b = self.b
        b.points = [(0, 0)] * 24
        for i in range(6):
            b.points[i] = (WHITE, 2)
        b.borne_off[WHITE] = 3
        self.assertTrue(b.can_bear_off_with_die(WHITE, 3))
        # Si tiene una en la barra, no puede
        b.bar[WHITE] = 1
        self.assertFalse(b.can_bear_off_with_die(WHITE, 3))

    # ----------------------------------------------------------
    # 6. BEAR OFF PIECE
    # ----------------------------------------------------------
    def test_bear_off_piece_exact_and_search(self):
        b = self.b
        b.points = [(0, 0)] * 24
        b.points[0] = (WHITE, 2)
        b.bear_off_piece(WHITE, 0, range(5, -1, -1))
        self.assertEqual(b.points[0], (WHITE, 1))
        self.assertEqual(b.borne_off[WHITE], 1)
        b.points[0] = (0, 0)
        b.points[3] = (WHITE, 1)
        b.bear_off_piece(WHITE, 0, range(5, -1, -1))
        self.assertEqual(b.borne_off[WHITE], 2)

    # ----------------------------------------------------------
    # 7. HIT TESTS
    # ----------------------------------------------------------
    def test_apply_hit_if_any(self):
        b = self.b
        b.points[10] = (BLACK, 1)
        b.apply_hit_if_any(WHITE, 10)
        self.assertEqual(b.bar[BLACK], 1)
        self.assertEqual(b.points[10], (0, 0))
        b.points[5] = (BLACK, 2)
        b.apply_hit_if_any(WHITE, 5)
        self.assertEqual(b.points[5], (BLACK, 2))  # No golpea si hay más de una

    # ----------------------------------------------------------
    # 8. MOVE CHECKER - casos completos
    # ----------------------------------------------------------
    def test_move_checker_from_bar_success_and_blocked(self):
        b = self.b
        b.bar[WHITE] = 1
        b.points[23] = (0, 0)
        self.assertTrue(b.move_checker(WHITE, None, 1))
        self.assertEqual(b.bar[WHITE], 0)
        # bloqueado
        b.bar[WHITE] = 1
        b.points[23] = (BLACK, 2)
        self.assertFalse(b.move_checker(WHITE, None, 1))

    def test_move_checker_normal_and_blocked(self):
        b = self.b
        b.points[23] = (WHITE, 1)
        b.points[22] = (0, 0)
        self.assertTrue(b.move_checker(WHITE, 23, 1))
        b.points[22] = (BLACK, 3)
        self.assertFalse(b.move_checker(WHITE, 23, 1))

    def test_move_checker_bearing_off_success_and_fail(self):
        b = self.b
        b.points = [(0, 0)] * 24
        for i in range(6):
            b.points[i] = (WHITE, 2)
        b.borne_off[WHITE] = 3
        b.bar[WHITE] = 0
        self.assertTrue(b.bearing_off_allowed(WHITE))
        self.assertTrue(b.move_checker(WHITE, 0, 6))
        # Caso fallido (bar con ficha)
        b.bar[WHITE] = 1
        self.assertFalse(b.move_checker(WHITE, 0, 6))

    def test_move_checker_invalid_owner_or_empty(self):
        b = self.b
        b.points[5] = (0, 0)
        self.assertFalse(b.move_checker(WHITE, 5, 1))
        b.points[5] = (BLACK, 1)
        self.assertFalse(b.move_checker(WHITE, 5, 1))

    # ----------------------------------------------------------
    # 9. RESET
    # ----------------------------------------------------------
    def test_reset(self):
        b = self.b
        b.points[0] = (WHITE, 3)
        b.bar[WHITE] = 2
        b.borne_off[BLACK] = 4
        b.reset()
        self.assertEqual(b.points[23], (WHITE, 2))
        self.assertEqual(b.bar[WHITE], 0)
        self.assertEqual(b.borne_off[BLACK], 0)


if __name__ == "__main__":
    unittest.main()
