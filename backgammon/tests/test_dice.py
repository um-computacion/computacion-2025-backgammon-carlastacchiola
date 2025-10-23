import unittest
from backgammon.core.dice import Dice


class TestDice(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test."""
        self.dice = Dice()

    # --------------------------
    # Inicialización
    # --------------------------
    def test_init_values_empty(self):
        """Los dados deben inicializarse sin valores."""
        self.assertEqual(self.dice.get_values(), [])

    # --------------------------
    # Tirada de un solo dado
    # --------------------------
    def test_roll_single_in_range(self):
        """El dado simple siempre debe estar entre 1 y 6."""
        for _ in range(100):
            value = self.dice.roll_single()
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 6)
            self.assertEqual(self.dice.get_values(), [value])

    # --------------------------
    # Tirada de dos dados
    # --------------------------
    def test_roll_two_dice_in_range(self):
        """Los dos dados deben tener valores entre 1 y 6."""
        for _ in range(100):
            values = self.dice.roll()
            self.assertEqual(len(values), 2)
            for v in values:
                self.assertGreaterEqual(v, 1)
                self.assertLessEqual(v, 6)
            self.assertEqual(self.dice.get_values(), values)

    # --------------------------
    # Tiradas dobles
    # --------------------------
    def test_is_double_true(self):
        """Debe detectar correctamente una tirada doble."""
        # Forzamos el valor directamente (sin usar random)
        self.dice.values= [4, 4]
        self.assertTrue(self.dice.is_double())

    def test_is_double_false(self):
        """Debe detectar correctamente una tirada no doble."""
        self.dice._Dice__values__ = [2, 5]
        self.assertFalse(self.dice.is_double())

    # --------------------------
    # Representación de texto
    # --------------------------
    def test_str_no_values(self):
        """Debe mostrar mensaje adecuado cuando no se han tirado dados."""
        self.assertEqual(str(self.dice), "Dados sin tirar.")

    def test_str_single_die(self):
        """Debe mostrar el valor de un solo dado."""
        self.dice.values = [3]
        self.assertIn("Dado: 3", str(self.dice))

    def test_str_two_dice(self):
        """Debe mostrar ambos valores en una tirada doble."""
        self.dice.values = [5, 6]
        texto = str(self.dice)
        self.assertIn("Dados:", texto)
        self.assertIn("5", texto)
        self.assertIn("6", texto)


if __name__ == "__main__":
    unittest.main()
