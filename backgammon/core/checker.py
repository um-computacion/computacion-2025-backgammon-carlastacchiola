class Checker:
    """
    Representa una ficha individual del juego de Backgammon.

    Cada ficha pertenece a un jugador y puede estar en el tablero,
    capturada o retirada (borneada).
    """

    def __init__(self, color: str, position: int = None):
        """
        Inicializa una ficha con un color y una posición opcional.

        Args:
            color (str): Color de la ficha (por ejemplo, 'blanco' o 'negro').
            position (int, opcional): Número del punto en el tablero (1–24).
                Si es None, significa que la ficha está fuera del tablero.

        Raises:
            TypeError: Si el color no es una cadena o la posición no es un entero.
            ValueError: Si la posición está fuera del rango 1–24.
        """
        if not isinstance(color, str):
            raise TypeError("El color debe ser una cadena de texto (str).")

        if position is not None:
            if not isinstance(position, int):
                raise TypeError("La posición debe ser un número entero.")
            if not (1 <= position <= 24):
                raise ValueError("La posición debe estar entre 1 y 24.")

        self.__color__ = color
        self.__position__ = position
        self.__captured__ = False
        self.__borne_off__ = False

    # =====================
    # GETTERS
    # =====================
    def get_color(self) -> str:
        """Devuelve el color de la ficha."""
        return self.__color__

    def get_position(self) -> int:
        """Devuelve la posición actual de la ficha (1–24 o None)."""
        return self.__position__

    def is_captured(self) -> bool:
        """Indica si la ficha está capturada (en la barra)."""
        return self.__captured__

    def is_borne_off(self) -> bool:
        """Indica si la ficha ya fue retirada del tablero."""
        return self.__borne_off__

    # =====================
    # ACCIONES
    # =====================
    def move_to(self, new_position: int):
        """
        Mueve la ficha a una nueva posición del tablero.

        Args:
            new_position (int): Punto de destino (1–24).

        Raises:
            ValueError: Si la ficha está capturada o borneada.
            TypeError: Si la posición no es un número entero.
        """
        if self.__captured__:
            raise ValueError("No se puede mover una ficha capturada.")
        if self.__borne_off__:
            raise ValueError("No se puede mover una ficha que ya fue retirada.")
        if not isinstance(new_position, int):
            raise TypeError("La nueva posición debe ser un número entero.")
        if not (1 <= new_position <= 24):
            raise ValueError("La posición debe estar entre 1 y 24.")

        self.__position__ = new_position

    def capture(self):
        """
        Marca la ficha como capturada (en la barra).
        """
        self.__captured__ = True
        self.__position__ = None

    def reenter(self, position: int):
        """
        Reingresa una ficha capturada al tablero.

        Args:
            position (int): Nueva posición de ingreso (1–24).

        Raises:
            ValueError: Si la ficha no está capturada.
        """
        if not self.__captured__:
            raise ValueError("Solo se pueden reingresar fichas capturadas.")
        if not (1 <= position <= 24):
            raise ValueError("La posición de reingreso debe estar entre 1 y 24.")

        self.__captured__ = False
        self.__position__ = position

    def bear_off(self):
        """
        Retira la ficha del tablero (bearing off).
        """
        self.__borne_off__ = True
        self.__position__ = None

    # =====================
    # REPRESENTACIÓN
    # =====================
    def __str__(self) -> str:
        """
        Devuelve una descripción legible de la ficha.
        """
        if self.__borne_off__:
            estado = "retirada del tablero"
        elif self.__captured__:
            estado = "capturada"
        elif self.__position__:
            estado = f"en la posición {self.__position__}"
        else:
            estado = "sin posición definida"

        return f"Ficha {self.__color__} ({estado})"
