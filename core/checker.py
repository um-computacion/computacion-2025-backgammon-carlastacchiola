# backgammon/core/checker.py


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
        self.color = color      # WHITE o BLACK
        self.position = None    # índice 0..23 o None si está fuera del tablero
        self.on_bar = False     # True si está en la barra
        self.borne_off = False  # True si ya fue sacada del tablero

    def __repr__(self):
        color_name = "Blanca" if self.color == WHITE else "Negra"
        state = (
            "fuera del tablero" if self.borne_off else
            "en barra" if self.on_bar else
            f"en punto {self.position + 1 if self.position is not None else '?'}"
        )
        return f"<Checker {color_name} ({state})>"

    # ----------------------------------------------------------
    # Métodos de estado
    # ----------------------------------------------------------
    def move_to_point(self, idx):
        """Actualiza la posición al índice del tablero."""
        self.position = idx
        self.on_bar = False
        self.borne_off = False

    def send_to_bar(self):
        """Envía la ficha a la barra."""
        self.position = None
        self.on_bar = True
        self.borne_off = False

    def bear_off(self):
        """Marca la ficha como retirada del tablero."""
        self.position = None
        self.on_bar = False
        self.borne_off = True

    def is_active(self):
        """True si la ficha sigue en juego (no borne_off)."""
        return not self.borne_off
