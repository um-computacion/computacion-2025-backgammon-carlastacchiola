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