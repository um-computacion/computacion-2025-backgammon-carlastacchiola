#CLI --> Interfaz de texto 

from backgammon.core.dice import Dice

#def decide_first_player():
    #dice = Dice()
    #jugador1 = dice.roll_single()
    #jugador2 = dice.roll_single()

    #if jugador1 > jugador2:
        #return "Jugador 1", [jugador1, jugador2]
    #elif jugador2 > jugador1:
        #return "Jugador 2", [jugador1, jugador2]
    #else:
        #return "Empate", [jugador1, jugador2]


#def main():
    #print("Decidiendo quién comienza la partida...\n")
    #winner, values = decide_first_player()

    #print(f"Jugador 1 tiró: {values[0]}")
    #print(f"Jugador 2 tiró: {values[1]}")

    #if winner != "Empate":
        #print(f" {winner} comienza la partida.")
    #else:
        #print(" Empate, volver a tirar.")


#if __name__ == "__main__":
    #main()

from backgammon.core.backgammon_game import BackgammonGame
from backgammon.core.player import Player


def main():
    print("🎯 Bienvenido al Backgammon (modo consola) 🎲\n")

    # Crear juego y jugadores
    game = BackgammonGame()
    name1 = input("Nombre del Jugador 1: ") or "Jugador 1"
    name2 = input("Nombre del Jugador 2: ") or "Jugador 2"
    p1 = Player(1, name1, "blanco")
    p2 = Player(2, name2, "negro")
    game.add_player(p1)
    game.add_player(p2)
    game.start_new_game()

    while True:
        print("\n" + "=" * 60)
        print(game.game_summary())
        print("=" * 60)

        current = game.get_current_player()
        print(f"\nTurno de {current.get_name()}")

        # Menú simple
        print("\nOpciones:")
        print("1. Tirar los dados 🎲")
        print("2. Mover una ficha 🚶")
        print("3. Terminar turno 🔁")
        print("4. Ver tablero 🧩")
        print("5. Salir ❌")

        choice = input("\nElegí una opción: ").strip()

        if choice == "1":
            values = game.roll_for_turn()
            print(f"\nDados tirados: {values}")

        elif choice == "2":
            try:
                start = int(input("Desde punto: "))
                end = int(input("Hasta punto: "))
                die = int(input("Valor del dado a usar: "))
                ok, msg = game.apply_move(start, end, die)
                print(msg)
            except ValueError:
                print("Entrada inválida. Intentá de nuevo.")

        elif choice == "3":
            game.end_turn()
            print("\nTurno terminado. Cambiando jugador...")

        elif choice == "4":
            print("\nEstado del tablero:")
            print(game.get_board())

        elif choice == "5":
            print("\nGracias por jugar 💫")
            break

        else:
            print("Opción inválida, intentá otra vez.")


if __name__ == "__main__":
    main()
