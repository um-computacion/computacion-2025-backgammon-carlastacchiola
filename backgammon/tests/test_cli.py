# backgammon/tests/test_cli.py
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from backgammon.cli.cli import CLI
from backgammon.core.board import WHITE, BLACK


class FakeGame:
    """Game falso para probar CLI sin lógica real."""
    def __init__(self):
        self.current_player = WHITE
        self.points = [(0, 0)] * 24
        self.bar = {WHITE: 0, BLACK: 0}
        self.borne_off = {WHITE: 0, BLACK: 0}
        self.dice = MagicMock()
        self.dice.values = [1, 6]
        self.dice.is_empty.return_value = False
        self._game_over = False

    def roll_dice(self): return (1, 6)
    def any_move_available(self, *_): return True
    def try_move(self, *_): return False
    def try_combined_move(self, src, dice_list): return dice_list == [1, 6]
    def switch_turn(self):
        self.current_player = BLACK
        self._game_over = True
    def is_game_over(self): return self._game_over
    def winner(self): return WHITE


class TestCLI(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_board_basic_output(self, mock_stdout):
        """Cubre print_board directamente."""
        cli = CLI()
        cli.game = FakeGame()
        cli.print_board()
        out = mock_stdout.getvalue()
        self.assertIn("ESTADO DEL TABLERO", out)
        self.assertIn("Turno actual:", out)
        self.assertIn("24:", out)  # asegura que recorrió el for

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_combined_move_and_victory(self, mock_stdout):
        """Cubre flujo normal con movimiento combinado y victoria."""
        cli = CLI()
        cli.game = FakeGame()
        cli.player_names = {WHITE: "Blanco", BLACK: "Negro"}

        inputs = iter(["", "13 1+6", "fin"])
        with patch("builtins.input", lambda *a: next(inputs)):
            cli.start()

        out = mock_stdout.getvalue()
        self.assertIn("Movimiento combinado con dados [1, 6].", out)
        self.assertIn("¡Ganó Blanco! ", out)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_invalid_and_unavailable_die(self, mock_stdout):
        """Cubre entrada inválida y dado no disponible."""
        cli = CLI()
        cli.game = FakeGame()
        cli.player_names = {WHITE: "Blanco", BLACK: "Negro"}

        inputs = iter(["", "invalido", "13 9", "fin"])
        with patch("builtins.input", lambda *a: next(inputs)):
            cli.start()

        out = mock_stdout.getvalue()
        self.assertIn("Formato inválido", out)
        self.assertIn(" Ese dado no está disponible.", out)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_handles_undefined_winner(self, mock_stdout):
        """Cubre caso donde el ganador no está en player_names."""
        cli = CLI()
        cli.game = FakeGame()
        cli.game.winner = lambda: 999  # ganador inexistente
        cli.player_names = {WHITE: "Blanco", BLACK: "Negro"}

        inputs = iter(["", "fin"])
        with patch("builtins.input", lambda *a: next(inputs)):
            cli.start()

        out = mock_stdout.getvalue()
        self.assertIn("Juego terminado sin ganador definido.", out)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_start_prints_welcome_and_exits_immediately(self, mock_stdout):
        """Cubre el inicio de CLI.start() (mensajes de bienvenida)."""
        cli = CLI()
        cli.game.is_game_over = lambda: True  # hace que termine enseguida
        cli.start()
        out = mock_stdout.getvalue()
        self.assertIn(" Bienvenido al Backgammon", out)
        self.assertIn("Jugadores:", out)

    def test_cli_can_be_instantiated(self):
        """Verifica que CLI puede crearse correctamente."""
        cli = CLI()
        self.assertIsNotNone(cli.game)
        self.assertIn(WHITE, cli.player_names)
        self.assertIn(BLACK, cli.player_names)

    def test_cli_start_ends_immediately_when_game_over(self):
        """Cubre el inicio de CLI.start() sin entrar al bucle."""
        cli = CLI()
        cli.game.is_game_over = lambda: True  
        cli.start()  


if __name__ == "__main__":
    unittest.main()
