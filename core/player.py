# backgammon/core/player.py

from .checker import Checker

WHITE = 1
BLACK = -1


class Player:
    """Representa un jugador (humano) con sus fichas individuales."""

    def __init__(self, name, color):
        self.__name__ = name
        self.__color__ = color
        self.__checkers_off__ = 0   # cuántas fichas ya sacó
        self.__on_bar__ = 0         # cuántas fichas están en la barra
        self.__checkers__ = [Checker(color) for _ in range(15)]  # fichas individuales

    # ----------------------------------------------------------
    # Estado del jugador
    # ----------------------------------------------------------
    def reset(self):
        """Reinicia estado general del jugador."""
        self.__checkers_off__ = 0
        self.__on_bar__ = 0
        for checker in self.__checkers__:
            checker.__position__ = None
            checker.__on_bar__ = False
            checker.__borne_off__ = False

    def borne_off_count(self):
        """Cantidad de fichas retiradas del tablero."""
        return len([c for c in self.__checkers__ if c.__borne_off__])

    def bar_count(self):
        """Cantidad de fichas actualmente en la barra."""
        return len([c for c in self.__checkers__ if c.__on_bar__])

    def active_checkers(self):
        """Devuelve la lista de fichas aún en juego."""
        return [c for c in self.__checkers__ if not c.__borne_off__]

    def __repr__(self):
        color_name = "Blanco" if self.__color__ == WHITE else "Negro"
        return f"Player({self.__name__}, {color_name})"