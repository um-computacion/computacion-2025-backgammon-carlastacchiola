class Player:
    """
    Representa un jugador de Backgammon.
    
    Gestiona el estado de un jugador incluyendo sus fichas en juego,
    fichas capturadas, fichas sacadas del tablero y puntuación.
    """

    def __init__(self, id: int, name: str, color: str):
        """
        Inicializa un nuevo jugador.
        
        Args:
            id (int): Identificador único del jugador (1 o 2).
            name (str): Nombre del jugador.
            color (str): Color de las fichas del jugador.
        
        Returns:
            None
        """
        # Identificación y datos
        self.__id__ = id
        self.__name__ = name
        self.__color__ = color

        # Estado del juego
        self.__checkers__ = 15  # Fichas activas en el tablero
        self.__captured__ = 0   # Fichas en la barra (capturadas)
        self.__borne_off__ = 0  # Fichas sacadas del tablero (ganadas)
        self.__score__ = 0      # Puntuación acumulada
        self.__turns__ = 0      # Cantidad de turnos jugados
        self.__history__ = []   # Historial de acciones

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
        
        Args:
            None
        
        Returns:
            int: Puntuación actual del jugador.
        """
        return self.__score__

    def get_id(self) -> int:
        """
        Obtiene el identificador del jugador.
        
        Args:
            None
        
        Returns:
            int: ID del jugador.
        """
        return self.__id__
    
    def get_name(self) -> str:
        """
        Obtiene el nombre del jugador.
        
        Args:
            None
        
        Returns:
            str: Nombre del jugador.
        """
        return self.__name__

    def get_color(self) -> str:
        """
        Obtiene el color de las fichas del jugador.
        
        Args:
            None
        
        Returns:
            str: Color del jugador.
        """
        return self.__color__
    
    def set_color(self, color: str):
        """
        Establece un nuevo color para el jugador.
        
        Args:
            color (str): Nuevo color para el jugador.
        
        Returns:
            None
        """
        self.__color__ = color
    
    def get_checkers(self) -> int:
        """
        Obtiene la cantidad de fichas activas en el tablero.
        
        Args:
            None
        
        Returns:
            int: Cantidad de fichas en juego.
        """
        return self.__checkers__
    
    def get_captured(self) -> int:
        """
        Obtiene la cantidad de fichas capturadas (en la barra).
        
        Args:
            None
        
        Returns:
            int: Cantidad de fichas capturadas.
        """
        return self.__captured__
    
    def get_borne_off(self) -> int:
        """
        Obtiene la cantidad de fichas sacadas del tablero.
        
        Args:
            None
        
        Returns:
            int: Cantidad de fichas fuera del juego.
        """
        return self.__borne_off__
    
    def get_turns(self) -> int:
        """
        Obtiene la cantidad de turnos jugados.
        
        Args:
            None
        
        Returns:
            int: Número de turnos jugados.
        """
        return self.__turns__

    def get_history(self) -> list:
        """
        Obtiene el historial completo de acciones del jugador.
        
        Args:
            None
        
        Returns:
            list: Lista con todas las acciones realizadas.
        """
        return self.__history__.copy()

    def add_history(self, action: str):
        """
        Agrega una acción al historial del jugador.
        
        Args:
            action (str): Descripción de la acción realizada.
        
        Returns:
            None
        """
        self.__history__.append(action)

    def capture_checker(self):
        """
        Captura una ficha del tablero y la envía a la barra.
        
        Args:
            None
        
        Returns:
            None
        
        Raises:
            ValueError: Si no hay fichas disponibles para capturar.
        """
        if self.__checkers__ <= 0:
            raise ValueError("No hay fichas disponibles para capturar")
        
        self.__checkers__ -= 1
        self.__captured__ += 1
        self.add_history("capturó ficha")

    def reenter_checker(self):
        """
        Reingresa una ficha desde la barra al tablero.
        
        Args:
            None
        
        Returns:
            None
        
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
        
        Args:
            None
        
        Returns:
            None
        
        Raises:
            ValueError: Si no hay fichas disponibles para sacar.
        """
        if self.__checkers__ <= 0:
            raise ValueError("No hay fichas disponibles para sacar")
        
        self.__checkers__ -= 1
        self.__borne_off__ += 1
        self.add_history("sacó ficha del tablero")

    def add_turn(self):
        """
        Incrementa el contador de turnos jugados.
        
        Args:
            None
        
        Returns:
            None
        """
        self.__turns__ += 1
        self.add_history(f"jugó turno #{self.__turns__}")

    def has_won(self) -> bool:
        """
        Verifica si el jugador ha ganado la partida.
        Un jugador gana cuando ha sacado todas sus 15 fichas del tablero.
        Args:
            None
        Returns:
            bool: True si el jugador ganó, False en caso contrario.
        """
        return self.__borne_off__ == 15

    def can_move(self) -> bool:
        """
        Verifica si el jugador puede realizar movimientos.
        Args:
            None       
        Returns:
            bool: True si tiene fichas para mover, False en caso contrario.
        """
        return self.__checkers__ > 0 or self.__captured__ > 0

    def __str__(self) -> str:
        """
        Representación en string del estado del jugador.
        Args:
            None
        Returns:
            str: Descripción del estado actual del jugador.
        """
        return (f"Jugador {self.__name__} ({self.__color__}) - "
                f"Fichas: {self.__checkers__}, Capturadas: {self.__captured__}, "
                f"Sacadas: {self.__borne_off__}, Puntos: {self.__score__}")

    