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
        # Negras: su casa está en 18–23
        for i in range(18, 24):
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

    def test_can_bear_off_and_move_checker_bearing_off(self):
        b = Board()
        b.points = [(0, 0)] * 24
        # Blancas en su casa (0–5)
        for i in range(6):
            b.points[i] = (WHITE, 2)
        b.borne_off[WHITE] = 3
        b.bar[WHITE] = 0
        # Ahora debe permitir sacar fichas
        self.assertTrue(b.bearing_off_allowed(WHITE))
        self.assertTrue(b.can_bear_off_with_die(WHITE, 6))
        self.assertTrue(b.move_checker(WHITE, 5, 6))
        # Si tiene fichas en la barra, no puede
        b.bar[WHITE] = 1
        self.assertFalse(b.bearing_off_allowed(WHITE))

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

    # ----------------------------------------------------------
    # 10. Cobertura extra de casos límite y alternativos
    # ----------------------------------------------------------

    def test_bearing_off_allowed_false_due_to_bar(self):
        """ Verifica que bearing_off_allowed() devuelva False si hay fichas en la barra."""
        b = Board()
        for i in range(24):
            b.points[i] = (0, 0)
        for i in range(0, 6):
            b.points[i] = (WHITE, 2)
        b.bar[WHITE] = 1  # hay fichas golpeadas
        self.assertFalse(b.bearing_off_allowed(WHITE))

    def test_bear_off_piece_fallback_search(self):
        """ Cubre la rama donde no hay ficha exacta en el índice y se busca en el rango."""
        b = Board()
        b.points = [(0, 0)] * 24
        b.points[3] = (WHITE, 1)  # no está en el índice pedido
        b.bear_off_piece(WHITE, 0, range(5, -1, -1))
        self.assertEqual(b.borne_off[WHITE], 1)

    def test_move_checker_blocked_returns_false(self):
        """ Asegura que move_checker() devuelva False si el punto destino está bloqueado."""
        b = Board()
        b.points[10] = (WHITE, 1)
        b.points[9] = (BLACK, 3)  # bloqueado por el oponente
        self.assertFalse(b.move_checker(WHITE, 10, 1))



    # ----------------------------------------------------------
    # 11. Cobertura adicional de ramas no ejecutadas en Board
    # ----------------------------------------------------------

    def test_can_bear_off_false_when_piece_outside_home(self):
        """✅ Verifica que can_bear_off() devuelva False si hay una ficha fuera del home_range."""
        b = Board()
        b.points = [(0, 0)] * 24
        # Blancas tienen fichas dentro y una afuera
        for i in range(0, 6):
            b.points[i] = (WHITE, 2)
        b.points[10] = (WHITE, 1)
        self.assertFalse(b.can_bear_off(WHITE))

    def test_can_bear_off_true_when_all_in_home_for_black(self):
        """✅ Verifica que las fichas negras puedan hacer bear_off cuando están en 18–23."""
        b = Board()
        b.points = [(0, 0)] * 24
        for i in range(18, 24):
            b.points[i] = (BLACK, 2)
        self.assertTrue(b.can_bear_off(BLACK))

    def test_apply_hit_if_any_and_blocked_cases(self):
        """✅ Cubre golpe exitoso y caso sin golpe (más de una ficha enemiga)."""
        b = Board()
        b.points = [(0, 0)] * 24
        # Golpe exitoso
        b.points[10] = (BLACK, 1)
        b.apply_hit_if_any(WHITE, 10)
        self.assertEqual(b.bar[BLACK], 1)
        # Caso sin golpe (más de una ficha enemiga)
        b.points[5] = (BLACK, 2)
        b.apply_hit_if_any(WHITE, 5)
        self.assertEqual(b.bar[BLACK], 1)  # no cambia

    def test_can_bear_off_with_die_white_false_when_piece_behind(self):
        """Cubre rama donde una ficha blanca no puede sacar por ficha más atrás."""
        b = Board()
        # Todas dentro de la casa excepto una detrás
        for i in range(0, 6):
            b.points[i] = (WHITE, 1)
        b.points[6] = (WHITE, 1)  # fuera del rango de casa
        self.assertFalse(b.can_bear_off_with_die(WHITE, 6))

    def test_can_bear_off_with_die_black_true_edge_case(self):
        """Cubre rama de éxito para ficha negra sacando con dado exacto (15 fichas en casa)."""
        b = Board()
        b.points = [(0, 0)] * 24
        distrib = [3, 3, 3, 3, 3, 0]  
        for i, cnt in enumerate(distrib, start=18):
            if cnt > 0:
                b.points[i] = (BLACK, cnt)
        b.borne_off[BLACK] = 0
        b.bar[BLACK] = 0
        self.assertTrue(b.bearing_off_allowed(BLACK))
        self.assertTrue(b.can_bear_off_with_die(BLACK, 6))

    def test_distance_to_bear_off_white_and_black(self):
        """Verifica que distance_to_bear_off calcule correctamente ambos colores."""
        b = Board()
        self.assertEqual(b.distance_to_bear_off(WHITE, 4), 5)
        self.assertEqual(b.distance_to_bear_off(BLACK, 20), 4)

    def test_apply_hit_if_any_adds_to_bar(self):
        """Cubre rama de apply_hit_if_any cuando se golpea una ficha del rival."""
        b = Board()
        b.points[5] = (BLACK, 1)
        b.apply_hit_if_any(WHITE, 5)
        self.assertEqual(b.bar[BLACK], 1)
        self.assertEqual(b.points[5], (0, 0))

    def test_move_checker_bearing_off_for_white(self):
        """Cubre movimiento válido donde una ficha blanca sale del tablero (15 fichas en casa)."""
        b = Board()
        b.points = [(0, 0)] * 24
        distrib = [3, 3, 3, 3, 3, 0]  
        for i, cnt in enumerate(distrib):
            if cnt > 0:
                b.points[i] = (WHITE, cnt)
        b.borne_off[WHITE] = 0
        b.bar[WHITE] = 0
        self.assertTrue(b.bearing_off_allowed(WHITE))
        moved = b.move_checker(WHITE, 0, 6)
        self.assertTrue(moved)
        self.assertEqual(b.borne_off[WHITE], 1)

    def test_reset_resets_everything(self):
        """Verifica que reset() deje el tablero igual al inicial."""
        b = Board()
        b.points[0] = (WHITE, 5)
        b.bar[BLACK] = 2
        b.borne_off[WHITE] = 3
        b.reset()
        # Chequea consistencia con setup inicial
        whites = sum(cnt for owner, cnt in b.points if owner == WHITE)
        blacks = sum(cnt for owner, cnt in b.points if owner == BLACK)
        self.assertEqual(whites, 15)
        self.assertEqual(blacks, 15)
        self.assertEqual(b.bar[WHITE], 0)
        self.assertEqual(b.bar[BLACK], 0)
        self.assertEqual(b.borne_off[WHITE], 0)
        self.assertEqual(b.borne_off[BLACK], 0)


    # ----------------------------------------------------------
    # 12. Casos finales para cubrir ramas específicas faltantes
    # ----------------------------------------------------------

    def test_bearing_off_allowed_true_exact_15_fichas(self):
        """✅ Cubre la rama donde bearing_off_allowed() devuelve True (todas en casa sin barra)."""
        b = Board()
        b.points = [(0, 0)] * 24
        for i in range(0, 6):
            b.points[i] = (WHITE, 3)
        b.bar[WHITE] = 0
        b.borne_off[WHITE] = 0
        # Ajustamos a 15 fichas exactas
        b.points[5] = (WHITE, 0)
        self.assertTrue(b.bearing_off_allowed(WHITE))

    


















if __name__ == "__main__":
    unittest.main()
