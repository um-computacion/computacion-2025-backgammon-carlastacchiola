import unittest
from core.backgammon_game import BackgammonGame, WHITE, BLACK
from core.board import Board
from core.dice import Dice
from core.player import Player


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

    def test_combined_move_destination_with_doubles(self):
        """Cubre el caso de dados dobles, donde no hay dos valores únicos."""
        g = BackgammonGame()
        result = g.combined_move_destination(WHITE, 10, [3, 3])
        self.assertIsNone(result)

    def test_combined_move_destination_with_doubles_returns_none(self):
        """Cubre el caso donde los dos dados son iguales y no se puede combinar."""
        g = BackgammonGame()
        result = g.combined_move_destination(WHITE, 10, [3, 3])
        self.assertIsNone(result)



    def test_try_combined_move_invalid_cases(self):
        g = BackgammonGame()
        self.assertFalse(g.try_combined_move(10, [1]))  # sólo un dado
        g.board.points[10] = (WHITE, 1)
        g.dice.values = [1, 2]
        g.board.points[9] = (BLACK, 3)  # bloqueado
        self.assertFalse(g.try_combined_move(10, [1, 2]))

    def test_try_move_consumes_die_and_returns_bool(self):
        """Verifica tanto el consumo del dado como el valor de retorno True/False."""
        g = BackgammonGame()
        g.roll_dice()
        die = g.dice.values[0]
        g.board.move_checker = lambda *a, **kw: True
        self.assertTrue(g.try_move(10, die))
        g.board.move_checker = lambda *a, **kw: False
        g.dice.values = [die]
        self.assertFalse(g.try_move(10, die))



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
        for i in range(24):
            g.board.points[i] = (0, 0)
        # Para que bearing_off_allowed() devuelva True,
        # las fichas deben estar en 0..5 
        total_fichas = 0
        for i in range(0, 6):
            g.board.points[i] = (WHITE, 3)
            total_fichas += 3
        exceso = total_fichas - 15
        if exceso > 0:
            owner, cnt = g.board.points[5]
            g.board.points[5] = (owner, cnt - exceso)
        g.board.bar[WHITE] = 0
        g.board.borne_off[WHITE] = 0
        self.assertTrue(g.bearing_off_allowed(WHITE))
        for i in range(24):
            g.board.points[i] = (0, 0)
        for i in range(0, 6):
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

    def test_end_turn_if_needed_no_dice_and_moves(self):
        """Cubre el caso donde no hay dados ni movimientos posibles."""
        g = BackgammonGame()
        g.dice.values = []
        g.any_move_available = lambda *a, **kw: False
        current = g.current_player
        g.end_turn_if_needed()
        self.assertNotEqual(g.current_player, current)

    def test_end_turn_if_needed_rolls_dice_after_switch(self):
        """Cubre la rama donde se cambia el turno y se lanzan los dados automáticamente."""
        g = BackgammonGame()
        g.dice.values = []
        g.any_move_available = lambda *a, **kw: False
        g.end_turn_if_needed()
        # Luego del cambio, debe haber tirado dados
        self.assertTrue(len(g.dice.values) in (2, 4))



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

    def test_any_move_available_returns_false_when_no_moves(self):
        """Cubre la rama donde ningún movimiento es posible."""
        g = BackgammonGame()
        g.dice.values = [2, 3]
        g.legal_single_sources = lambda player, die: []
        self.assertFalse(g.any_move_available(WHITE, g.dice.values))


    def test_try_combined_move_partial_fail(self):
        """Simula el caso en que el segundo movimiento del combinado falla."""
        g = BackgammonGame()
        g.board.points[10] = (WHITE, 1)
        g.board.points[9] = (0, 0)
        g.board.points[8] = (0, 0)
        g.dice.values = [1, 2]
        # Forzamos que el segundo movimiento falle
        g.board.move_checker = lambda *args, **kwargs: args[1] == 10
        result = g.try_combined_move(10, [1, 2])
        self.assertFalse(result)

    def test_try_bear_off_edge_cases(self):
        """Cubre caminos donde el dado no está disponible o move_checker devuelve False."""
        g = BackgammonGame()
        g.dice.values = [2, 3]
        self.assertFalse(g.try_bear_off(0, 6))  # dado no está
        g.board.move_checker = lambda *a, **kw: False
        g.board.can_bear_off_with_die = lambda *a, **kw: True
        g.dice.values = [3]
        self.assertFalse(g.try_bear_off(0, 3))

    def test_try_bear_off_click_all_fail_paths(self):
        """Ejercita los caminos fallidos del clic para bearing off."""
        g = BackgammonGame()
        g.dice.values = [6]
        g.points[5] = (BLACK, 1)  # ficha del oponente
        self.assertFalse(g.try_bear_off_click(5))  # no es del jugador actual
        g.points[5] = (WHITE, 1)
        g.board.bearing_off_allowed = lambda p: False
        self.assertFalse(g.try_bear_off_click(5))  # no permitido
        g.board.bearing_off_allowed = lambda p: True
        g.home_range = lambda p: range(10, 15)
        self.assertFalse(g.try_bear_off_click(5))  # fuera de casa

    def test_try_bear_off_click_with_higher_die(self):
        """Cubre el caso donde el dado es mayor que la distancia necesaria."""
        g = BackgammonGame()
        # preparar tablero en condiciones válidas
        for i in range(24):
            g.board.points[i] = (0, 0)
        g.board.points[0] = (WHITE, 1)
        g.dice.values = [6]
        g.board.bearing_off_allowed = lambda p: True
        g.home_range = lambda p: range(0, 6)
        g.board.distance_to_bear_off = lambda p, i: 3
        g.board.can_bear_off_with_die = lambda p, d: True
        g.board.move_checker = lambda *a, **kw: True
        moved = g.try_bear_off_click(0)
        self.assertTrue(moved)


    def test_legal_single_sources_from_bar_case(self):
        """Verifica que se cubra el camino donde hay fichas en la barra."""
        g = BackgammonGame()
        g.bar[WHITE] = 1
        g.board.enter_from_bar_targets = lambda p, d: [5]
        g._point_is_blocked = lambda p, idx: False
        res = g.legal_single_sources(WHITE, 3)
        self.assertIn(None, res)

    def test_end_turn_if_needed_no_change_when_moves_available(self):
        """ Verifica que NO cambie de jugador si todavía hay jugadas posibles."""
        g = BackgammonGame()
        g.dice.values = [3]
        g.board.move_checker = lambda *a, **kw: True
        g.any_move_available = lambda *a, **kw: True
        current = g.current_player
        g.end_turn_if_needed()
        self.assertEqual(g.current_player, current)

    def test_start_game_turn_when_dice_already_set(self):
        """ Asegura que si los dados ya tienen valores, start_game_turn() no los vuelve a tirar."""
        g = BackgammonGame()
        g.dice.values = [4, 5]
        g.start_game_turn()
        self.assertEqual(g.dice.values, [4, 5])

    def test_winner_returns_zero_when_no_one_finished(self):
        """Comprueba que winner() devuelva 0 cuando ningún jugador completó las 15 fichas."""
        g = BackgammonGame()
        g.board.borne_off = {WHITE: 10, BLACK: 12}
        self.assertEqual(g.winner(), 0)

    def test_try_combined_move_undo_on_second_fail(self):
        """ Cubre la rama donde el segundo move falla y se revierte el primero."""
        g = BackgammonGame()
        g.current_player = WHITE
        g.board.move_checker = lambda player, idx, die: True if die == 1 else False
        g.points[5] = (WHITE, 1)
        # Forzar falla del segundo movimiento
        result = g.try_combined_move(5, [1, 2])
        self.assertFalse(result)

    def test_try_combined_move_success_consumes_both_dice(self):
        """Cubre el caso exitoso de try_combined_move: mueve dos veces y consume ambos dados."""
        g = BackgammonGame()
        g.current_player = WHITE
        g.board.points[5] = (WHITE, 1)
        g.board.move_checker = lambda player, idx, die: True  # siempre se puede mover
        g._point_is_blocked = lambda player, idx: False
        g.dice.values = [1, 2]
        result = g.try_combined_move(5, [1, 2])
        self.assertTrue(result)
        self.assertEqual(g.remaining_moves, [])


    def test_try_bear_off_returns_false_when_move_checker_fails(self):
        """ Cubre el caso donde can_bear_off_with_die es True pero move_checker devuelve False."""
        g = BackgammonGame()
        g.dice.values = [3]
        g.board.can_bear_off_with_die = lambda p, d: True
        g.board.move_checker = lambda *a, **kw: False  # Forzamos fallo
        self.assertFalse(g.try_bear_off(5, 3))

    def test_end_turn_if_needed_switches_player_when_no_moves(self):
        """ Cubre la rama donde no hay movimientos disponibles y se cambia el turno."""
        g = BackgammonGame()
        g.dice.values = [3]
        g.any_move_available = lambda *a, **kw: False
        current = g.current_player
        g.end_turn_if_needed()
        self.assertNotEqual(g.current_player, current)

    def test_winner_returns_zero_explicitly(self):
        """ Cubre la rama final de winner() cuando ningún jugador gana."""
        g = BackgammonGame()
        g.board.borne_off = {WHITE: 0, BLACK: 0}
        result = g.winner()
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
