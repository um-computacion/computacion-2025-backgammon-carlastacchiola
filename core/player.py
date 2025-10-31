# backgammon/core/player.py

from .checker import Checker

WHITE = 1
BLACK = -1


class Player:
    """Representa un jugador (humano) con sus fichas individuales."""

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.checkers_off = 0   # cuántas fichas ya sacó
        self.on_bar = 0         # cuántas fichas están en la barra
        self.checkers = [Checker(color) for _ in range(15)]  # fichas individuales

    # ----------------------------------------------------------
    # Estado del jugador
    # ----------------------------------------------------------
    def reset(self):
        """Reinicia estado general del jugador."""
        self.checkers_off = 0
        self.on_bar = 0
        for checker in self.checkers:
            checker.position = None
            checker.on_bar = False
            checker.borne_off = False

    def borne_off_count(self):
        """Cantidad de fichas retiradas del tablero."""
        return len([c for c in self.checkers if c.borne_off])

    def bar_count(self):
        """Cantidad de fichas actualmente en la barra."""
        return len([c for c in self.checkers if c.on_bar])

    def active_checkers(self):
        """Devuelve la lista de fichas aún en juego."""
        return [c for c in self.checkers if not c.borne_off]

    def __repr__(self):
        color_name = "Blanco" if self.color == WHITE else "Negro"
        return f"Player({self.name}, {color_name})"
