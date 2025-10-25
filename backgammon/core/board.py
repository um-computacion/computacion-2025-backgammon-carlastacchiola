from typing import List, Tuple


class Board:
    """
    Representa el tablero de Backgammon.
    Mantiene el estado de los 24 puntos, las fichas en la barra
    y las fichas que han sido retiradas (bearing off).
    """

    # Posiciones iniciales estándar simplificadas.
    # Cada clave representa un punto (1–24).
    # El valor es una tupla (cantidad_fichas, id_jugador).
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
        Crea los puntos (1–24), las barras y los contadores de fichas retiradas.
        """
        # Cada punto es una tupla (cantidad_fichas, id_jugador).
        self._points: List[Tuple[int, int]] = [(0, 0) for _ in range(26)]  # 0 y 25 reservados

        # Fichas en la barra
        self._bar_player1 = 0
        self._bar_player2 = 0

        # Fichas retiradas del tablero (bearing off)
        self._borne_off_player1 = 0
        self._borne_off_player2 = 0

        # Historial de movimientos realizados
        self._move_history: List[Tuple[int, int, int]] = []

        # Configurar posición inicial
        self._setup_initial_position()

    # -------------------------------------------------------------------------
    # Inicialización y estado general
    # -------------------------------------------------------------------------
    def _setup_initial_position(self):
        """
        Configura el tablero con la posición inicial estándar de Backgammon.
        Reemplaza los puntos vacíos por las posiciones definidas en INITIAL_POSITION.
        """
        for i in range(1, 25):
            self._points[i] = (0, 0)
        for point, (count, player) in self.INITIAL_POSITION.items():
            self._points[point] = (count, player)

    def get_point(self, position: int) -> Tuple[int, int]:
        """
        Devuelve el estado de un punto específico del tablero.

        Args:
            position (int): número del punto (1–24).

        Returns:
            tuple: (cantidad_fichas, id_jugador)

        Raises:
            ValueError: si la posición está fuera del rango válido.
        """
        if not (1 <= position <= 24):
            raise ValueError("La posición debe estar entre 1 y 24.")
        return self._points[position]

    def get_all_points(self) -> List[Tuple[int, int]]:
        """
        Devuelve el estado completo del tablero.

        Returns:
            list: lista de 24 tuplas (cantidad_fichas, id_jugador).
        """
        return self._points[1:25].copy()

    def get_bar(self, player_id: int) -> int:
        """
        Devuelve la cantidad de fichas en la barra de un jugador.

        Args:
            player_id (int): ID del jugador (1 o 2).

        Returns:
            int: cantidad de fichas en la barra.

        Raises:
            ValueError: si el ID de jugador no es válido.
        """
        if player_id == 1:
            return self._bar_player1
        elif player_id == 2:
            return self._bar_player2
        else:
            raise ValueError("El ID de jugador debe ser 1 o 2.")

    def get_borne_off(self, player_id: int) -> int:
        """
        Devuelve la cantidad de fichas retiradas (bearing off) de un jugador.

        Args:
            player_id (int): ID del jugador (1 o 2).

        Returns:
            int: cantidad de fichas fuera del tablero.

        Raises:
            ValueError: si el ID de jugador no es válido.
        """
        if player_id == 1:
            return self._borne_off_player1
        elif player_id == 2:
            return self._borne_off_player2
        else:
            raise ValueError("El ID de jugador debe ser 1 o 2.")

    # -------------------------------------------------------------------------
    # Movimiento y validaciones
    # -------------------------------------------------------------------------
    def move_checker(self, start: int, end: int, player_id: int):
        """
        Mueve una ficha de un punto a otro según las reglas básicas del Backgammon.
        Maneja capturas y puntos bloqueados.

        Args:
            start (int): punto de origen (1–24).
            end (int): punto de destino (1–24).
            player_id (int): jugador que realiza el movimiento (1 o 2).

        Raises:
            ValueError: si las posiciones o el movimiento son inválidos.
        """
        if not (1 <= start <= 24 and 1 <= end <= 24):
            raise ValueError("Las posiciones deben estar entre 1 y 24.")
        if player_id not in (1, 2):
            raise ValueError("El ID de jugador debe ser 1 o 2.")

        count_s, owner_s = self._points[start]
        if count_s == 0 or owner_s != player_id:
            raise ValueError(f"No hay fichas del jugador {player_id} en el punto {start}.")

        count_e, owner_e = self._points[end]

        # Caso 1: punto vacío
        if owner_e == 0:
            self._points[end] = (1, player_id)

        # Caso 2: mismo jugador
        elif owner_e == player_id:
            self._points[end] = (count_e + 1, player_id)

        # Caso 3: captura (una ficha rival sola)
        elif count_e == 1 and owner_e != player_id:
            self._points[end] = (1, player_id)
            if owner_e == 1:
                self._bar_player1 += 1
            else:
                self._bar_player2 += 1

        # Caso 4: punto bloqueado (dos o más fichas rivales)
        else:
            raise ValueError(f"Punto {end} bloqueado por el jugador {owner_e}.")

        # Actualizar punto de origen
        if count_s - 1 == 0:
            self._points[start] = (0, 0)
        else:
            self._points[start] = (count_s - 1, player_id)

        # Registrar movimiento
        self._move_history.append((player_id, start, end))

    # -------------------------------------------------------------------------
    # Bearing off y barra
    # -------------------------------------------------------------------------
    def bear_off_checker(self, player_id: int):
        """
        Retira una ficha del tablero (bearing off).

        Args:
            player_id (int): jugador que realiza la acción.

        Raises:
            ValueError: si el ID es inválido.
        """
        if player_id == 1:
            self._borne_off_player1 += 1
        elif player_id == 2:
            self._borne_off_player2 += 1
        else:
            raise ValueError("El ID de jugador debe ser 1 o 2.")

    def add_to_bar(self, player_id: int):
        """
        Agrega una ficha a la barra del jugador indicado (por captura).

        Args:
            player_id (int): jugador que recibe la ficha capturada.

        Raises:
            ValueError: si el ID de jugador no es válido.
        """
        if player_id == 1:
            self._bar_player1 += 1
        elif player_id == 2:
            self._bar_player2 += 1
        else:
            raise ValueError("El ID de jugador debe ser 1 o 2.")

    def reenter_from_bar(self, player_id: int):
        """
        Reingresa una ficha desde la barra al tablero.

        Args:
            player_id (int): jugador que reingresa una ficha.

        Raises:
            ValueError: si no hay fichas en la barra o el ID es inválido.
        """
        if player_id == 1 and self._bar_player1 > 0:
            self._bar_player1 -= 1
        elif player_id == 2 and self._bar_player2 > 0:
            self._bar_player2 -= 1
        else:
            raise ValueError("No hay fichas en la barra para este jugador.")

    # -------------------------------------------------------------------------
    # Métodos auxiliares
    # -------------------------------------------------------------------------
    def load_points(self, points: List[Tuple[int, int]]):
        """
        Carga un estado completo de los puntos del tablero.

        Args:
            points (list): lista con 24 tuplas (cantidad, jugador_id).

        Raises:
            ValueError: si la lista no tiene 24 elementos.
        """
        if len(points) != 24:
            raise ValueError("La lista de puntos debe tener 24 elementos.")
        for i, value in enumerate(points, start=1):
            self._points[i] = value

    def get_history(self) -> List[Tuple[int, int, int]]:
        """
        Devuelve el historial completo de movimientos realizados.

        Returns:
            list: lista de tuplas (player_id, start, end).
        """
        return self._move_history.copy()

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
        Devuelve una representación legible del estado actual del tablero.

        Returns:
            str: texto con la información de cada punto, la barra y los borne-offs.
        """
        lines = ["=== Estado actual del tablero ==="]
        for i in range(1, 25):
            count, player = self._points[i]
            if count > 0:
                lines.append(f"Punto {i:>2}: {count} fichas del jugador {player}")
        lines.append(f"Barra → J1: {self._bar_player1}, J2: {self._bar_player2}")
        lines.append(f"Borne Off → J1: {self._borne_off_player1}, J2: {self._borne_off_player2}")
        return "\n".join(lines)
