
from typing import List, Tuple

class Board:
    """
    Representa el tablero de Backgammon.
    Mantiene el estado de los 24 puntos, las fichas en la barra
    y las fichas que han sido retiradas (bearing off).
    """

    # Posiciones iniciales estándar simplificadas
    # Cada clave representa un punto (1-24)
    # El valor es una tupla (cantidad_fichas, id_jugador)
    INITIAL_POSITION = {
        1: (2, 1),
        6: (5, 2),
        8: (3, 2),
        12: (5, 1),
        13: (5, 2),
        17: (3, 1),
        19: (5, 1),
        24: (2, 2),
    }

    def __init__(self):
        """
        Inicializa el tablero de Backgammon con posiciones estándar.
        Crea los puntos (1–24), la barra y los contadores de fichas sacadas.
        """
        # Cada punto es una tupla (cantidad_fichas, id_jugador)
        # 0 → vacío
        self.__points__ = [(0, 0) for _ in range(26)]  # 0–25 (0 y 25 usados internamente)

        # Contadores de fichas en la barra
        self.__bar_player1__ = 0
        self.__bar_player2__ = 0

        # Contadores de fichas fuera del tablero (bearing off)
        self.__borne_off_player1__ = 0
        self.__borne_off_player2__ = 0

        # Historial de movimientos
        self.__move_history__ = []

        # Inicializar con la posición estándar
        self._setup_initial_position()

    # -------------------------------------------------------------------------
    # Inicialización y estado general
    # -------------------------------------------------------------------------
    def _setup_initial_position(self):
        """
        Configura el tablero con la posición inicial estándar de Backgammon.
        """
        for point, (count, player) in self.INITIAL_POSITION.items():
            self.__points__[point] = (count, player)

    def get_point(self, position: int) -> Tuple[int, int]:
        """
        Devuelve el estado de un punto específico del tablero.
        Args:
            position (int): número del punto (1–24)
        Returns:
            tuple: (cantidad_fichas, id_jugador)
        Raises:
            ValueError: si la posición está fuera del rango válido.
        """
        if position < 1 or position > 24:
            raise ValueError(f"Posición inválida: {position}. Debe estar entre 1 y 24.")
        return self.__points__[position]

    def get_all_points(self) -> List[Tuple[int, int]]:
        """
        Devuelve el estado de todos los puntos (1–24).
        Returns:
            list: lista de tuplas (cantidad_fichas, id_jugador)
        """
        return self.__points__[1:25].copy()

    def get_bar(self, player_id: int) -> int:
        """
        Devuelve la cantidad de fichas en la barra del jugador indicado.
        Args:
            player_id (int): 1 o 2
        Returns:
            int: cantidad de fichas capturadas
        Raises:
            ValueError: si el id es inválido
        """
        if player_id == 1:
            return self.__bar_player1__
        elif player_id == 2:
            return self.__bar_player2__
        else:
            raise ValueError("El ID de jugador debe ser 1 o 2.")

    def get_borne_off(self, player_id: int) -> int:
        """
        Devuelve la cantidad de fichas que el jugador ha sacado del tablero.
        Args:
            player_id (int): 1 o 2
        Returns:
            int: cantidad de fichas fuera del tablero
        Raises:
            ValueError: si el id es inválido
        """
        if player_id == 1:
            return self.__borne_off_player1__
        elif player_id == 2:
            return self.__borne_off_player2__
        else:
            raise ValueError("El ID de jugador debe ser 1 o 2.")

    # -------------------------------------------------------------------------
    # Movimiento y validaciones
    # -------------------------------------------------------------------------
    def move_checker(self, start: int, end: int, player_id: int):
        """
        Mueve una ficha de un punto a otro siguiendo reglas básicas del Backgammon.
        Maneja capturas simples y valida puntos bloqueados.
        Args:
            start (int): punto de origen (1–24)
            end (int): punto de destino (1–24)
            player_id (int): jugador que mueve (1 o 2)
        Raises:
            ValueError: si el movimiento es inválido o bloqueado
        """
        if not (1 <= start <= 24 and 1 <= end <= 24):
            raise ValueError("Las posiciones deben estar entre 1 y 24.")

        count_s, owner_s = self.__points__[start]
        if count_s == 0 or owner_s != player_id:
            raise ValueError(f"No hay fichas del jugador {player_id} en el punto {start}.")

        count_e, owner_e = self.__points__[end]

        # Caso 1: punto destino vacío
        if owner_e == 0:
            self.__points__[end] = (1, player_id)

        # Caso 2: punto destino ocupado por el mismo jugador
        elif owner_e == player_id:
            self.__points__[end] = (count_e + 1, player_id)

        # Caso 3: punto destino con una sola ficha del rival (captura)
        elif count_e == 1 and owner_e != player_id:
            self.__points__[end] = (1, player_id)
            if owner_e == 1:
                self.__bar_player1__ += 1
            else:
                self.__bar_player2__ += 1

        # Caso 4: punto bloqueado (dos o más fichas del rival)
        else:
            raise ValueError(f"Punto {end} bloqueado por el jugador {owner_e}.")

        # Actualizar origen
        if count_s - 1 == 0:
            self.__points__[start] = (0, 0)
        else:
            self.__points__[start] = (count_s - 1, player_id)

        # Registrar movimiento
        self.__move_history__.append((player_id, start, end))

    # -------------------------------------------------------------------------
    # Métodos de soporte
    # -------------------------------------------------------------------------
    def bear_off_checker(self, player_id: int):
        """
        Saca una ficha del tablero (bearing off).
        Args:
            player_id (int): jugador que realiza el movimiento
        Raises:
            ValueError: si no hay fichas disponibles
        """
        if player_id == 1:
            self.__borne_off_player1__ += 1
        elif player_id == 2:
            self.__borne_off_player2__ += 1
        else:
            raise ValueError("El ID de jugador debe ser 1 o 2.")

    def load_points(self, points: List[Tuple[int, int]]):
        """
        Carga un estado completo de puntos (para restaurar partidas guardadas).
        Args:
            points (list): lista de 24 tuplas (count, player_id)
        Raises:
            ValueError: si la lista no tiene 24 elementos
        """
        if len(points) != 24:
            raise ValueError("La lista de puntos debe tener 24 elementos.")
        for i, value in enumerate(points, start=1):
            self.__points__[i] = value

    def get_history(self) -> List[Tuple[int, int, int]]:
        """
        Devuelve el historial completo de movimientos realizados.
        Returns:
            list: lista de tuplas (player_id, start, end)
        """
        return self.__move_history__.copy()

    def reset_board(self):
        """
        Reinicia el tablero al estado inicial estándar.
        """
        self.__init__()

    # -------------------------------------------------------------------------
    # Representación legible
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """
        Devuelve una representación legible del estado del tablero.
        Returns:
            str: resumen del estado del tablero.
        """
        lines = ["=== Estado actual del tablero ==="]
        for i in range(1, 25):
            count, player = self.__points__[i]
            lines.append(f"Punto {i:>2}: {count} fichas del jugador {player}")
        lines.append(f"Barra J1: {self.__bar_player1__}, Barra J2: {self.__bar_player2__}")
        lines.append(f"Borne Off J1: {self.__borne_off_player1__}, J2: {self.__borne_off_player2__}")
        return "\n".join(lines)
