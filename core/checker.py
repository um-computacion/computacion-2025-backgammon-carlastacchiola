# core/checker.py


from core.board import WHITE, BLACK

WHITE = 1
BLACK = -1


class Checker:
    """
    Representa una ficha individual en el Backgammon.
    No maneja coordenadas por sí misma; su posición
    se determina por el índice de punto en el Board.
    """

    def __init__(self, color):
        self.__color__ = color      # WHITE o BLACK
        self.__position__ = None    # índice 0..23 o None si está fuera del tablero
        self.__on_bar__ = False     # True si está en la barra
        self.__borne_off__ = False  # True si ya fue sacada del tablero

    def __repr__(self):
        color_name = "Blanca" if self.__color__ == WHITE else "Negra"
        state = (
            "fuera del tablero" if self.__borne_off__ else
            "en barra" if self.__on_bar__ else
            f"en punto {self.__position__ + 1 if self.__position__ is not None else '?'}"
        )
        return f"<Checker {color_name} ({state})>"

    # ----------------------------------------------------------
    # Métodos de estado
    # ----------------------------------------------------------
    def move_to_point(self, idx):
        """Actualiza la posición al índice del tablero."""
        self.__position__ = idx
        self.__on_bar__ = False
        self.__borne_off__ = False

    def send_to_bar(self):
        """Envía la ficha a la barra."""
        self.__position__ = None
        self.__on_bar__ = True
        self.__borne_off__ = False

    def bear_off(self):
        """Marca la ficha como retirada del tablero."""
        self.__position__ = None
        self.__on_bar__ = False
        self.__borne_off__ = True

    def is_active(self):
        """True si la ficha sigue en juego (no borne_off)."""
        return not self.__borne_off__