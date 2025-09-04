
from core.dice import Dice

def main():
    dice = Dice()

    print("Decidiendo quién comienza la partida...\n")

    jugador1 = dice.roll_single()
    jugador2 = dice.roll_single()

    print(f"Jugador 1 tiró: {jugador1}")
    print(f"Jugador 2 tiró: {jugador2}")

    if jugador1 > jugador2:
        print("El Jugador 1 comienza la partida.")
        first_turn = [jugador1, jugador2]  
    elif jugador2 > jugador1:
        print("El Jugador 2 comienza la partida.")
        first_turn = [jugador1, jugador2]  