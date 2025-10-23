class Player:
    """
    Representa a un jugador de Backgammon.
    
    Gestiona el estado de un jugador, incluyendo sus fichas activas,
    fichas capturadas, fichas sacadas del tablero (borne off),
    historial de acciones, cantidad de turnos y puntuación.
    """

    def __init__(self, id: int, name: str, color: str):
        """
        Inicializa un nuevo jugador.

        Args:
            id (int): Identificador único del jugador (1 o 2).
            name (str): Nombre del jugador.
            color (str): Color de las fichas del jugador.

        Raises:
            TypeError: Si los tipos de los parámetros son incorrectos.
        """
        # Validación de tipos básicos
        if not isinstance(id, int):
            raise TypeError("El id debe ser un número entero")
        if not isinstance(name, str):
            raise TypeError("El nombre debe ser un texto")
        if not isinstance(color, str):
            raise TypeError("El color debe ser un texto")

        # Identificación y datos
        self.__id__ = id
        self.__name__ = name
        self.__color__ = color

        # Estado del juego
        self.__checkers__ = 15   # Fichas activas en el tablero
        self.__captured__ = 0    # Fichas en la barra (capturadas)
        self.__borne_off__ = 0   # Fichas sacadas del tablero
        self.__score__ = 0       # Puntuación acumulada
        self.__turns__ = 0       # Turnos jugados
        self.__history__ = []    # Historial de acciones

    # =====================
    # MÉTODOS DE PUNTAJE
    # =====================
    def add_score(self, points: int):
        """
        Suma puntos al marcador del jugador.

        Args:
            points (int): Cantidad de puntos a sumar.

        Returns:
            None
        """
        self.__score__ += points

    def get_score(self) -> int:
        """
        Obtiene la puntuación actual del jugador.

        Returns:
            int: Puntuación actual del jugador.
        """
        return self.__score__

    # =====================
    # GETTERS / SETTERS
    # =====================
    def get_id(self) -> int:
        """Devuelve el identificador único del jugador."""
        return self.__id__

    def get_name(self) -> str:
        """Devuelve el nombre del jugador."""
        return self.__name__

    def get_color(self) -> str:
        """Devuelve el color de las fichas del jugador."""
        return self.__color__

    def set_color(self, color: str):
        """
        Establece un nuevo color de fichas para el jugador.

        Args:
            color (str): Nuevo color a asignar.
        """
        self.__color__ = color

    def get_checkers(self) -> int:
        """Devuelve la cantidad de fichas activas en el tablero."""
        return self.__checkers__

    def get_captured(self) -> int:
        """Devuelve la cantidad de fichas en la barra (capturadas)."""
        return self.__captured__

    def get_borne_off(self) -> int:
        """Devuelve la cantidad de fichas sacadas del tablero."""
        return self.__borne_off__

    def get_turns(self) -> int:
        """Devuelve la cantidad de turnos jugados."""
        return self.__turns__

    def get_history(self) -> list:
        """Devuelve una copia del historial de acciones del jugador."""
        return self.__history__.copy()

    # =====================
    # ACCIONES DE JUEGO
    # =====================
    def capture_checker(self):
        """
        Captura una ficha del tablero y la envía a la barra.

        Raises:
            ValueError: Si no hay fichas activas para capturar.
        """
        if self.__checkers__ <= 0:
            raise ValueError("No hay fichas disponibles para capturar")

        self.__checkers__ -= 1
        self.__captured__ += 1
        self.add_history("capturó ficha")

    def reenter_checker(self):
        """
        Reingresa una ficha desde la barra al tablero.

        Raises:
            ValueError: Si no hay fichas capturadas para reingresar.
        """
        if self.__captured__ <= 0:
            raise ValueError("No hay fichas capturadas para reingresar")

        self.__captured__ -= 1
        self.__checkers__ += 1
        self.add_history("reingresó ficha")

    def bear_off_checker(self):
        """
        Saca una ficha definitivamente del tablero (bearing off).

        Raises:
            ValueError: Si no hay fichas disponibles para sacar.
        """
        if self.__checkers__ <= 0:
            raise ValueError("No hay fichas disponibles para sacar")

        self.__checkers__ -= 1
        self.__borne_off__ += 1
        self.add_history("sacó ficha del tablero")

    def add_turn(self):
        """Incrementa el contador de turnos jugados y lo registra en el historial."""
        self.__turns__ += 1
        self.add_history(f"jugó turno #{self.__turns__}")

    # =====================
    # ESTADO DEL JUGADOR
    # =====================
    def has_won(self) -> bool:
        """
        Verifica si el jugador ha ganado la partida.
        Gana cuando saca las 15 fichas del tablero.

        Returns:
            bool: True si ganó, False en caso contrario.
        """
        return self.__borne_off__ == 15  # gana al sacar las 15 fichas

    def can_move(self) -> bool:
        """
        Verifica si el jugador puede mover fichas.

        Returns:
            bool: True si tiene fichas activas o capturadas.
        """
        return self.__checkers__ > 0 or self.__captured__ > 0

    def reset(self):
        """
        Reinicia el estado del jugador para una nueva partida.
        """
        self.__checkers__ = 15
        self.__captured__ = 0
        self.__borne_off__ = 0
        self.__score__ = 0
        self.__turns__ = 0
        self.__history__.clear()

    # =====================
    # HISTORIAL / RESUMEN
    # =====================
    def add_history(self, action: str):
        """Agrega una acción al historial del jugador."""
        self.__history__.append(action)

    def summary(self) -> dict:
        """
        Devuelve un resumen del estado actual del jugador.

        Returns:
            dict: Información completa del jugador.
        """
        return {
            "id": self.__id__,
            "name": self.__name__,
            "color": self.__color__,
            "checkers": self.__checkers__,
            "captured": self.__captured__,
            "borne_off": self.__borne_off__,
            "score": self.__score__,
            "turns": self.__turns__,
        }

    # =====================
    # REPRESENTACIÓN
    # =====================
    def __str__(self) -> str:
        """
        Representación en string del estado del jugador.

        Returns:
            str: Descripción legible del estado actual.
        """
        return (f"Jugador {self.__name__} ({self.__color__}) - "
                f"Fichas: {self.__checkers__}, Capturadas: {self.__captured__}, "
                f"Sacadas: {self.__borne_off__}, Puntos: {self.__score__}")
