from core.dice import Dice

def decide_first_player():
    dice = Dice()
    jugador1 = dice.roll_single()
    jugador2 = dice.roll_single()

    if jugador1 > jugador2:
        return "Jugador 1", [jugador1, jugador2]
    elif jugador2 > jugador1:
        return "Jugador 2", [jugador1, jugador2]
    else:
        return "Empate", [jugador1, jugador2]

def main():
    print("Decidiendo quién comienza la partida...\n")

    winner, values = decide_first_player()

    print(f"Jugador 1 tiró: {values[0]}")
    print(f"Jugador 2 tiró: {values[1]}")

    if winner != "Empate":
        print(f"👉 {winner} comienza la partida.")
    else:
        print("⚖️ Empate, volver a tirar.")

if __name__ == "__main__":
    main()
