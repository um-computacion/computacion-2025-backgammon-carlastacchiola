class player:

    def __init__(self,id: int, name: str, color: str ):
        self.__id__ = id
        self.__name__ = name
        self.__color__ = color
        self.__checkers__ = 15
        self.__captured__ = 0
        self.__score__ = 0

    def add_score(self, points: int):
        self.__score__ += points

    def get_score(self) -> int:
        return self.__score__




    def get_name(self) -> str:
        return self.__name__
    
    def get_color(self) -> str:
        return self.__color__
    
    def get_checkers(self) ->int:
        return self.__checkers__
    
    def get_captured(self) -> int:
        return self.__captured__


    def capture_checker(self):
         if self.__checkers__ > 0:
            self.__checkers__ -= 1
            self.__captured__ += 1

    def reenter_checker(self):
        if self.__captured__ > 0:
            self.__captured__ -= 1
            self.__checkers__ += 1

    def has_won(self) -> bool:
        return self.__checkers__ == 0 and self.__captured__ == 0
    
    def bear_off_checker(self):
        if self.__checkers__ > 0:
            self.__checkers__ -= 1

    def __str__(self):
        return (f"Jugador {self.__name__} ({self.__color__}) "
                f"- Fichas: {self.__checkers__}, Capturadas: {self.__captured__}")
    
    def can_move(self) -> bool:
        return self.__checkers__ > 0 or self.__captured__ > 0

    