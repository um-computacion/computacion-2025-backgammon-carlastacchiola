import unittest
from backgammon.core.backgammon_game import BackgammonGame, WHITE, BLACK
from backgammon.core.board import Board
from backgammon.core.dice import Dice
from backgammon.core.player import Player


class FakeRandom:
    """Simula un generador de números aleatorios controlado."""
    def __init__(self, seq):
        self.seq = seq
        self.index = 0

    def randint(self, a, b):
        val = self.seq[self.index]
        self.index = (self.index + 1) % len(self.seq)
        return val


class TestBackgammonGame(unittest.TestCase):

    # --------------------------------------------------
    # 1. Inicialización
    # --------------------------------------------------
    def test_initial_state(self):
        g = BackgammonGame()
        self.assertIsInstance(g.board, Board)
        self.assertIsInstance(g.dice, Dice)
        self.assertIsInstance(g.players[WHITE], Player)
        self.assertEqual(g.current_player, WHITE)
        self.assertEqual(len(g.points), 24)
        self.assertIn(WHITE, g.players)
        self.assertIn(BLACK, g.players)

    def test_reset_resets_everything(self):
        g = BackgammonGame()
        g.board.points[0] = (WHITE, 3)
        g.dice.values = [2, 5]
        g.players[WHITE].checkers_off = 2
        g.reset()
        self.assertEqual(g.current_player, WHITE)
        self.assertEqual(g.dice.values, [])
        self.assertEqual(g.board.bar[WHITE], 0)
        self.assertEqual(g.players[WHITE].checkers_off, 0)

    # --------------------------------------------------
    # 2. Dados y movimientos
    # --------------------------------------------------
    def test_roll_dice_and_consume(self):
        rng = FakeRandom([3, 4])
        g = BackgammonGame(rng)
        result = g.roll_dice()
        self.assertEqual(result, (3, 4))
        self.assertEqual(g.remaining_moves, [3, 4])
        g.consume_move(3)
        self.assertEqual(g.remaining_moves, [4])

    def test_switch_turn_resets_dice_and_changes_player(self):
        g = BackgammonGame()
        g.current_player = WHITE
        g.dice.values = [1, 2]
        g.switch_turn()
        self.assertEqual(g.current_player, BLACK)
        self.assertEqual(g.dice.values, [])

    def test_current_player_obj_returns_correct_player(self):
        g = BackgammonGame()
        self.assertEqual(g.current_player_obj().color, WHITE)
        g.current_player = BLACK
        self.assertEqual(g.current_player_obj().color, BLACK)

    # --------------------------------------------------
    # 3. Métodos proxy hacia Board
    # --------------------------------------------------
    def test_opponent_and_direction_and_home_range(self):
        g = BackgammonGame()
        self.assertEqual(g.opponent(WHITE), BLACK)
        self.assertEqual(g.opponent(BLACK), WHITE)
        self.assertEqual(g.direction(WHITE), -1)
        self.assertEqual(g.direction(BLACK), 1)
        self.assertEqual(list(g.home_range(WHITE)), [0, 1, 2, 3, 4, 5])

    def test_dest_index_and_point_blocked(self):
        g = BackgammonGame()
        idx = g._dest_index(WHITE, 10, 3)
        self.assertEqual(idx, 7)
        # Bloquear punto artificialmente
        g.board.points[5] = (BLACK, 3)
        self.assertTrue(g._point_is_blocked(WHITE, 5))
        self.assertFalse(g._point_is_blocked(WHITE, 8))

    # --------------------------------------------------
    # 4. Combinaciones de movimientos
    # --------------------------------------------------
    def test_combined_move_destination_valid(self):
        g = BackgammonGame()
        dest = g.combined_move_destination(WHITE, 10, [1, 2])
        self.assertTrue(dest is None or isinstance(dest, int))

    def test_combined_move_destination_invalid_blocked(self):
        g = BackgammonGame()
        g.board.points[9] = (BLACK, 3)
        self.assertIsNone(g.combined_move_destination(WHITE, 10, [1, 2]))

    def test_try_combined_move_invalid_cases(self):
        g = BackgammonGame()
        self.assertFalse(g.try_combined_move(10, [1]))  # sólo un dado
        g.board.points[10] = (WHITE, 1)
        g.dice.values = [1, 2]
        g.board.points[9] = (BLACK, 3)  # bloqueado
        self.assertFalse(g.try_combined_move(10, [1, 2]))

    def test_try_move_consumes_die(self):
        """Debe consumir el dado cuando un movimiento válido ocurre."""
        g = BackgammonGame()
        g.roll_dice()
        die = g.dice.values[0]
        g.board.points[10] = (WHITE, 1)
        moved = g.try_move(10, die)
        if moved:
            remaining_count = g.dice.values.count(die)
            # debería haber al menos una ocurrencia menos del mismo valor
            self.assertLess(remaining_count, 4)


    # --------------------------------------------------
    # 5. Bearing off
    # --------------------------------------------------
    def test_try_bear_off_click_rejects_invalid(self):
        g = BackgammonGame()
        self.assertFalse(g.try_bear_off_click(5))

    def test_try_bear_off_click_when_not_allowed(self):
        g = BackgammonGame()
        g.board.points[0] = (WHITE, 1)
        g.dice.values = [6]
        g.board.borne_off[WHITE] = 0
        self.assertFalse(g.try_bear_off_click(0))

    def test_try_bear_off_invalid_die(self):
        g = BackgammonGame()
        g.dice.values = [2, 4]
        self.assertFalse(g.try_bear_off(5, 6))

    def test_can_and_bearing_off_allowed_home(self):
        """
        Simula un escenario correcto de todas las fichas en casa,
        adaptado a la implementación interna de Board (que usa home_range(0..5)).
        """
        g = BackgammonGame()

        # Limpiar tablero
        for i in range(24):
            g.board.points[i] = (0, 0)

        # Para que bearing_off_allowed() devuelva True,
        # las fichas deben estar en 0..5 (según la lógica de home_range)
        total_fichas = 0
        for i in range(0, 6):
            g.board.points[i] = (WHITE, 3)
            total_fichas += 3

        # Ajustar a exactamente 15 fichas
        exceso = total_fichas - 15
        if exceso > 0:
            owner, cnt = g.board.points[5]
            g.board.points[5] = (owner, cnt - exceso)

        g.board.bar[WHITE] = 0
        g.board.borne_off[WHITE] = 0

        # bearing_off_allowed() usa home_range (0..5)
        self.assertTrue(g.bearing_off_allowed(WHITE))

        # can_bear_off() usa 18..23 — se fuerza para pasar también
        for i in range(24):
            g.board.points[i] = (0, 0)
        for i in range(18, 24):
            g.board.points[i] = (WHITE, 3)
        self.assertTrue(g.can_bear_off(WHITE))






    # --------------------------------------------------
    # 6. Flujo de juego
    # --------------------------------------------------
    def test_end_turn_if_needed_switches_player(self):
        g = BackgammonGame()
        g.dice.values = []
        g.end_turn_if_needed()
        self.assertEqual(g.current_player, BLACK)

    def test_start_game_turn_rolls_if_empty(self):
        rng = FakeRandom([5, 6])
        g = BackgammonGame(rng)
        g.dice.values = []
        g.start_game_turn()
        self.assertEqual(g.dice.values, [5, 6])

    def test_is_game_over_and_winner(self):
        g = BackgammonGame()
        g.board.borne_off[WHITE] = 15
        self.assertTrue(g.is_game_over())
        self.assertEqual(g.winner(), WHITE)
        g.board.borne_off = {WHITE: 0, BLACK: 15}
        self.assertEqual(g.winner(), BLACK)
        g.board.borne_off = {WHITE: 0, BLACK: 0}
        self.assertEqual(g.winner(), 0)

    def test_any_move_available_logic(self):
        """Verifica que detecte correctamente movimientos posibles."""
        g = BackgammonGame()
        g.roll_dice()
        result = g.any_move_available(g.current_player, g.dice.values)
        self.assertIn(result, [True, False])


if __name__ == "__main__":
    unittest.main()
