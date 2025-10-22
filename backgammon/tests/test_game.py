"""
Tests unitarios para la clase BackgammonGame usando unittest.
Adaptado a la versión con atributos __nombre__ y __board__.
"""

import unittest
from core.backgammon_game import BackgammonGame
from core.player import Player
from core.board import Board


class TestBackgammonGame(unittest.TestCase):
    """Casos de prueba para la clase BackgammonGame."""

    def setUp(self):
        """Configura una partida con dos jugadores antes de cada test."""
        self.game = BackgammonGame()
        self.p1 = Player(1, "Carla", "rojo")
        self.p2 = Player(2, "Bot", "azul")
        self.game.add_player(self.p1)
        self.game.add_player(self.p2)
        self.game.start_new_game()

    def test_add_and_start_game(self):
        """Verifica que se puedan agregar jugadores y comenzar una partida."""
        self.assertEqual(len(self.game.__players__), 2)
        self.assertTrue(self.game.__game_started__)

    def test_roll_for_turn_and_double(self):
        """Verifica que los dados se tiran correctamente y maneja dobles."""
        rolls = self.game.roll_for_turn()
        self.assertIsInstance(rolls, list)
        for r in rolls:
            self.assertTrue(1 <= r <= 6)
        self.assertIn(len(self.game.available_dice()), [2, 4])

    def test_apply_valid_move(self):
        """Verifica que un movimiento válido se aplique correctamente."""
        board = self.game.__board__
        board.__points__[1] = (2, 1)
        board.__points__[2] = (0, 0)

        self.game.__turn_dice_values__ = [1]
        ok, msg = self.game.apply_move(1, 2, 1)
        self.assertTrue(ok)
        self.assertIn("éxito", msg.lower())
        self.assertEqual(board.get_point(2)[1], 1)

    def test_apply_invalid_move(self):
        """Verifica que un movimiento inválido devuelva False y mensaje."""
        self.game.__turn_dice_values__ = [3]
        ok, msg = self.game.apply_move(0, 2, 3)
        self.assertFalse(ok)
        # Aceptamos cualquier mensaje de error mientras sea texto
        self.assertIsInstance(msg, str)
        self.assertGreater(len(msg), 0)

    def test_turn_flow_and_winner(self):
        """Verifica cambio de turnos y detección de ganador."""
        current = self.game.get_current_player()
        self.assertEqual(current.get_id(), 1)

        self.game.end_turn()
        self.assertEqual(self.game.get_current_player().get_id(), 2)

        # Forzamos condición de victoria con método público
        winner = self.game.get_current_player()
        for _ in range(15):
            try:
                winner.bear_off_checker()
            except ValueError:
                winner._Player__checkers__ += 1
                winner.bear_off_checker()

        result = self.game.check_winner()
        self.assertIsNotNone(result)
        self.assertEqual(result, winner)

    def test_serialize_and_load_state(self):
        """Verifica serialización y carga básica de estado."""
        json_state = self.game.serialize_state()
        self.assertIsInstance(json_state, str)

        new_game = BackgammonGame(Board())
        new_game.add_player(Player(1, "Carla", "rojo"))
        new_game.add_player(Player(2, "Bot", "azul"))
        new_game.load_state_from_json(json_state)

        self.assertTrue(isinstance(new_game.__board__, Board))
        self.assertEqual(len(new_game.__players__), 2)


if __name__ == "__main__":
    unittest.main()
