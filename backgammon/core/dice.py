# backgammon/core/dice.py
import random


class Dice:
    """Lógica de tiradas de los dados del Backgammon."""

    def __init__(self, rng=None):
        self.rng = rng or random.Random()
        self.values = []  # ejemplo: [3, 5] o [6, 6, 6, 6]

    def roll(self):
        """Tira los dados y devuelve una lista de valores disponibles."""
        d1 = self.rng.randint(1, 6)
        d2 = self.rng.randint(1, 6)
        if d1 == d2:
            self.values = [d1, d1, d1, d1]
        else:
            self.values = [d1, d2]
        return self.values

    def consume(self, value):
        """Elimina un valor del conjunto de movimientos disponibles."""
        if value in self.values:
            self.values.remove(value)

    def reset(self):
        """Vacía los dados (por ejemplo, al final del turno)."""
        self.values = []

    def is_empty(self):
        """Devuelve True si ya no quedan movimientos."""
        return len(self.values) == 0

    def __repr__(self):
        return f"Dice({self.values})"
