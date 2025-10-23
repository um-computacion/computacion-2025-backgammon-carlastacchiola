import random

class Dice:
    """
    Representa un par de dados utilizados en el juego de Backgammon.
    Permite realizar tiradas individuales o dobles y consultar los valores obtenidos.
    También identifica si se ha sacado una tirada doble.
    """

    def __init__(self):
        """Inicializa una nueva instancia de los dados."""
        self.values = []  # Lista con los valores de la última tirada

    # =====================
    # MÉTODOS PRINCIPALES
    # =====================
    def roll_single(self) -> int:
        """Realiza una tirada de un solo dado (1 al 6)."""
        value = random.randint(1, 6)
        self.values = [value]
        return value

    def roll(self) -> list:
        """Realiza una tirada de ambos dados."""
        self.values = [random.randint(1, 6), random.randint(1, 6)]
        return self.values

    def get_values(self) -> list:
        """Devuelve los valores obtenidos en la última tirada."""
        return self.values.copy()

    def is_double(self) -> bool:
        """Verifica si la última tirada fue doble (ambos dados iguales)."""
        return len(self.values) == 2 and self.values[0] == self.values[1]

    # =====================
    # REPRESENTACIÓN
    # =====================
    def __str__(self) -> str:
        """Representación en string del estado actual de los dados."""
        if not self.values:
            return "Dados sin tirar."
        elif len(self.values) == 1:
            return f"Dado: {self.values[0]}"
        else:
            return f"Dados: {self.values[0]} y {self.values[1]}"
