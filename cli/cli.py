# backgammon/cli/cli.py

from core.backgammon_game import BackgammonGame, WHITE, BLACK


class CLI:
    """
    Interfaz de línea de comandos (texto) para jugar o probar Backgammon.
    Permite visualizar el estado del tablero y hacer movimientos simples.
    """

    def __init__(self):
        self.game = BackgammonGame()
        self.player_names = {
            WHITE: "Jugador Blanco",
            BLACK: "Jugador Negro"
        }

    # ----------------------------------------------------------
    # Funciones de visualización
    # ----------------------------------------------------------
    def print_board(self):
        """Muestra el estado actual del tablero en texto simple."""
        print("\n=== ESTADO DEL TABLERO ===")
        print(f"Turno actual: {self.player_names[self.game.current_player]}")
        print(f"Dados: {self.game.dice.values}")
        print(f"Barra: Blanco={self.game.bar[WHITE]}, Negro={self.game.bar[BLACK]}")
        print(f"Fichas fuera: Blanco={self.game.borne_off[WHITE]}, Negro={self.game.borne_off[BLACK]}")
        print("-" * 40)
        for i in range(23, -1, -1):
            owner, count = self.game.points[i]
            if owner == WHITE:
                color = "W"
            elif owner == BLACK:
                color = "B"
            else:
                color = "."
            print(f"{i+1:2}: {color} x{count}")
        print("-" * 40)

    # ----------------------------------------------------------
    # Flujo principal de juego
    # ----------------------------------------------------------
    def start(self):
        """Inicia una partida interactiva por consola."""
        print(" Bienvenido al Backgammon (modo texto)")
        print("Jugadores:")
        print("  Blanco: mueve de 24 → 1")
        print("  Negro : mueve de 1 → 24")
        print()

        while not self.game.is_game_over():
            self.print_board()

            input(f"Presione Enter para tirar los dados ({self.player_names[self.game.current_player]})...")
            self.game.roll_dice()
            print(f"Dados: {self.game.dice.values}")

            while not self.game.dice.is_empty() and self.game.any_move_available(
                self.game.current_player, self.game.dice.values
            ):
                print(f"Movimientos restantes: {self.game.dice.values}")
                move = input("Ingrese movimiento (desde, dado o 'a+b' para combinar, 'fin' para pasar): ")

                if move.lower().startswith("fin"):
                    break

                try:
                    src_str, die_str = move.replace(",", " ").split()
                    src = int(src_str) - 1
                    if "+" in die_str:
                        dice_list = [int(x) for x in die_str.split("+")]
                        moved = self.game.try_combined_move(src, dice_list)
                        if moved:
                            print(f" Movimiento combinado con dados {dice_list}.")
                        else:
                            print(" Movimiento combinado no permitido.")
                        continue
                    else:
                        die = int(die_str)
                except ValueError:
                    print("Formato inválido. Ejemplo: '13 6' o '13,6'")
                    continue

                if die not in self.game.dice.values:
                    print(" Ese dado no está disponible.")
                    continue

                moved = self.game.try_move(src, die)
                if moved:
                    print(" Movimiento válido.")
                else:
                    print(" Movimiento no permitido.")

            print("Fin del turno.\n")
            self.game.switch_turn()

        # ---------- FIN DEL JUEGO ----------
        winner_color = self.game.winner()
        # Si no hay ganador definido (por ejemplo, durante tests), evitamos error
        if winner_color not in self.player_names:
            print("Juego terminado sin ganador definido.")
            return


        # Fin del juego
        ganador = self.player_names[self.game.winner()]
        print(f" ¡Ganó {ganador}! ")


if __name__ == "__main__":
    cli = CLI()
    cli.start()
