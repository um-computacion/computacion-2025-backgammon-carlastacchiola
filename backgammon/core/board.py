from typing import List, Optional, Tuple

def Board():
    
     # Posiciones iniciales estándar de Backgammon
    INITIAL_POSITION = {
        1: (2, 1),    # 2 fichas del jugador 1 en punto 1
        6: (5, 2),    # 5 fichas del jugador 2 en punto 6
        8: (3, 2),    # 3 fichas del jugador 2 en punto 8
        12: (5, 1),   # 5 fichas del jugador 1 en punto 12
        13: (5, 2),   # 5 fichas del jugador 2 en punto 13
        17: (3, 1),   # 3 fichas del jugador 1 en punto 17
        19: (5, 1),   # 5 fichas del jugador 1 en punto 19
        24: (2, 2),   # 2 fichas del jugador 2 en punto 24
    }

    def __init__(self):
        """
        Inicializa el tablero de Backgammon con las posiciones estándar.
        Args:
            None
        Returns:
            None
        """
        # Puntos del tablero: índice 0-25 (0=barra P1, 1-24=puntos, 25=barra P2)
        # Cada punto es una tupla (cantidad_fichas, id_jugador)
        # (0, 0) significa punto vacío
        self.__points__ = [(0, 0) for _ in range(26)]
        
        # Contadores de fichas en la barra
        self.__bar_player1__ = 0  # Fichas capturadas del jugador 1
        self.__bar_player2__ = 0  # Fichas capturadas del jugador 2
        
        # Contadores de fichas fuera del tablero (bearing off)
        self.__borne_off_player1__ = 0
        self.__borne_off_player2__ = 0
        
        # Historial de movimientos
        self.__move_history__ = []
        
        # Inicializar con posición estándar
        self._setup_initial_position()

    def _setup_initial_position(self):
        """
        Configura el tablero con la posición inicial estándar de Backgammon. 
        Args:
            None
        Returns:
            None
        """
        for point, (count, player) in self.INITIAL_POSITION.items():
            self.__points__[point] = (count, player)

    def get_point(self, position: int) -> Tuple[int, int]:
        """
        Obtiene el estado de un punto específico del tablero.
        Args:
            position (int): Número del punto (1-24).
        Returns:
            tuple: (cantidad_fichas, id_jugador) en ese punto.
        Raises:
            ValueError: Si la posición está fuera del rango válido.
        """
        if position < 1 or position > 24:
            raise ValueError(f"Posición inválida: {position}. Debe estar entre 1 y 24")
        
        return self.__points__[position]
