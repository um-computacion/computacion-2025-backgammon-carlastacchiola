# backgammon/tests/test_dice.py
import unittest
from core.dice import Dice


class FakeRandom:
    """Clase auxiliar para controlar los valores de los dados en los tests."""
    def __init__(self, seq):
        self.seq = seq
        self.index = 0

    def randint(self, a, b):
        val = self.seq[self.index]
        self.index = (self.index + 1) % len(self.seq)
        return val


class TestDice(unittest.TestCase):

    # --------------------------------------------------
    # 1. ROLL
    # --------------------------------------------------
    def test_roll_two_different_values(self):
        rng = FakeRandom([3, 5])
        d = Dice(rng)
        result = d.roll()
        self.assertEqual(result, [3, 5])
        self.assertEqual(d.values, [3, 5])
        # Repetir la tirada para confirmar que se actualiza
        rng.seq = [1, 2]
        result2 = d.roll()
        self.assertEqual(result2, [1, 2])
        self.assertEqual(d.values, [1, 2])

    def test_roll_doubles_creates_four_values(self):
        rng = FakeRandom([6, 6])
        d = Dice(rng)
        result = d.roll()
        self.assertEqual(result, [6, 6, 6, 6])
        self.assertEqual(len(result), 4)
        # Los valores deben ser todos iguales
        self.assertTrue(all(v == 6 for v in result))

    def test_roll_random_range_limits(self):
        """Verifica que los valores generados están dentro de 1-6."""
        d = Dice()
        for _ in range(20):
            vals = d.roll()
            for v in vals:
                self.assertIn(v, range(1, 7))

    # --------------------------------------------------
    # 2. CONSUME
    # --------------------------------------------------
    def test_consume_existing_value(self):
        d = Dice()
        d.values = [3, 5]
        d.consume(3)
        self.assertEqual(d.values, [5])

    def test_consume_nonexistent_value_does_nothing(self):
        d = Dice()
        d.values = [2, 4]
        d.consume(6)
        self.assertEqual(d.values, [2, 4])

    def test_consume_on_empty_list(self):
        d = Dice()
        d.values = []
        d.consume(3)
        self.assertEqual(d.values, [])

    def test_consume_removes_only_one_occurrence(self):
        """Si hay duplicados, solo elimina uno."""
        d = Dice()
        d.values = [4, 4, 5]
        d.consume(4)
        self.assertEqual(d.values.count(4), 1)
        self.assertEqual(d.values, [4, 5])

    # --------------------------------------------------
    # 3. RESET
    # --------------------------------------------------
    def test_reset_clears_values(self):
        d = Dice()
        d.values = [1, 2, 3]
        d.reset()
        self.assertEqual(d.values, [])
        self.assertTrue(d.is_empty())

    # --------------------------------------------------
    # 4. IS_EMPTY
    # --------------------------------------------------
    def test_is_empty_consistency(self):
        d = Dice()
        cases = [
            ([], True),
            ([1], False),
            ([1, 2], False),
        ]
        for values, expected in cases:
            with self.subTest(values=values):
                d.values = values
                self.assertEqual(d.is_empty(), expected)

    # --------------------------------------------------
    # 5. REPR
    # --------------------------------------------------
    def test_repr_output(self):
        d = Dice()
        d.values = [2, 5]
        self.assertEqual(repr(d), "Dice([2, 5])")
        d.reset()
        self.assertEqual(repr(d), "Dice([])")

    # --------------------------------------------------
    # 6. INTEGRACIÓN: flujo completo de turno
    # --------------------------------------------------
    def test_full_turn_flow(self):
        """Simula un flujo completo: tirar, consumir y resetear."""
        rng = FakeRandom([3, 3])
        d = Dice(rng)
        roll = d.roll()
        self.assertEqual(roll, [3, 3, 3, 3])

        # Consumir todos los valores
        for _ in range(4):
            d.consume(3)
        self.assertTrue(d.is_empty())

        # Reset al final del turno
        d.reset()
        self.assertEqual(d.values, [])
        self.assertTrue(d.is_empty())


if __name__ == "__main__":
    unittest.main()
