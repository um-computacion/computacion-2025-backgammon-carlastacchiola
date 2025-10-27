from typing import List, Tuple, Optional
import json

from backgammon.core.dice import Dice
from backgammon.core.player import Player
from backgammon.core.board import Board


class BackgammonGame:
    """
    Coordina la ejecución de una partida de Backgammon:
    - Mantiene el tablero (Board), los jugadores (Player) y los dados (Dice).
    - Expone operaciones para iniciar partida, ejecutar turnos, validar y aplicar movimientos,
      y verificar condiciones de victoria.
    Nota: Para mantener separación de responsabilidades, la lógica
    de movimientos puntuales (update de puntos) se delega a Board.move_checker
    si está disponible. Si no, BackgammonGame intentará operar con la API pública
    mínima de Board y fallará con una excepción clara para que Board implemente
    el método requerido.
    """

    def __init__(self, board: Optional[Board] = None):
        """
        Inicializa una nueva instancia de BackgammonGame.
        Args:
            board (Optional[Board]): Instancia del tablero. Si es None, se crea una nueva.
        """
        self.__board__ = board if board is not None else Board()
        self.__dice__ = Dice()
        self.__players__: List[Player] = []
        self.__current_player_index__: int = 0  # índice en self.__players__
        self.__turn_dice_values__: List[int] = []  # dados disponibles en el turno actual
        self.__is_double__ = False  # si la tirada actual es doble (usar 4 movimientos)
        self.__history__ = []  # historial de turnos y acciones
        self.__game_started__ = False

    # ---------------------- Gestión de jugadores ----------------------
    def add_player(self, player: Player):
        """
        Añade un jugador a la partida.
        Args:
            player (Player): instancia de Player (id debe ser 1 o 2).
        Raises:
            ValueError: si ya hay dos jugadores o el id no es válido.
        """
        if len(self.__players__) >= 2:
            raise ValueError("Ya existen dos jugadores en la partida.")
        if player.get_id() not in (1, 2):
            raise ValueError("Player.id debe ser 1 o 2.")
        self.__players__.append(player)

    def get_current_player(self) -> Player:
        """Devuelve el jugador cuyo turno es actualmente."""
        return self.__players__[self.__current_player_index__]
    
    def get_board(self) -> Board:
        """
        Devuelve el tablero actual del juego.

        Returns:
            Board: instancia del tablero asociada al juego.
        """
        return self.__board__
   


    def switch_turn(self):
        """Cambia el turno al siguiente jugador."""
        self.__current_player_index__ = 1 - self.__current_player_index__

    # ---------------------- Inicio y control de la partida ----------------------
    def start_new_game(self):
        """
        Marca el inicio de una nueva partida. Requiere exactamente 2 jugadores añadidos.
        Inicializa estado relevante.
        Raises:
            RuntimeError: si no hay exactamente 2 jugadores.
        """
        if len(self.__players__) != 2:
            raise RuntimeError("Se requieren exactamente 2 jugadores para iniciar la partida.")
        self.__game_started__ = True
        self.__history__.append({"action": "start_game", "players": [p.get_name() for p in self.__players__]})
        # Por convención, el jugador con id=1 será index 0; puede cambiarse por tirada de desempate.
        # No hacemos decidir primer jugador aquí: ese paso puede ser delegado al CLI.
        return True

    # ---------------------- Dados y tiradas ----------------------
    def roll_for_turn(self) -> List[int]:
        """
        Ejecuta la tirada de dados para el turno actual y prepara los valores disponibles.
        Maneja dobles (repiten 4 movimientos).
        Returns:
            List[int]: valores resultantes de la tirada (2 o 4 valores si es doble).
        """
        vals = self.__dice__.roll()
        if vals[0] == vals[1]:
            # dobles -> cuatro movimientos del mismo valor
            self.__is_double__ = True
            self.__turn_dice_values__ = [vals[0]] * 4
        else:
            self.__is_double__ = False
            self.__turn_dice_values__ = vals.copy()
        self.__history__.append({"action": "roll", "player": self.get_current_player().get_name(), "values": self.__turn_dice_values__.copy()})
        return self.__turn_dice_values__.copy()

    def consume_die(self, value: int):
        """
        Consume una ocurrencia de 'value' del conjunto de dados del turno.
        Raises:
            ValueError: si el valor solicitado no está disponible.
        """
        if value not in self.__turn_dice_values__:
            raise ValueError(f"Dado con valor {value} no disponible en esta tirada: {self.__turn_dice_values__}")
        self.__turn_dice_values__.remove(value)

    # ---------------------- Movimientos ----------------------
    def available_dice(self) -> List[int]:
        """Devuelve la lista de valores de dados aún disponibles en el turno."""
        return self.__turn_dice_values__.copy()

    def can_player_move(self, player: Player) -> bool:
        """
        Verifica de forma básica si el jugador puede mover:
        - Si tiene fichas en tablero o en barra.
        - NOTA: no comprueba movimientos específicos (bloqueos), solo estado global.
        """
        return player.can_move()

    def apply_move(self, start: int, end: int, die_value: int) -> Tuple[bool, str]:
        """
        Intenta aplicar un movimiento del punto `start` al punto `end` usando `die_value`.
        Verifica disponibilidad del dado y delega la actualización del tablero a Board.move_checker.
        Args:
            start (int): punto origen (1-24).
            end (int): punto destino (1-24).
            die_value (int): valor de dado a consumir.
        Returns:
            Tuple[bool, str]: (True, mensaje) si se aplicó; (False, razón) en error.
        Raises:
            RuntimeError / ValueError para errores criticós de uso.
        """
        if die_value not in self.__turn_dice_values__:
            return False, f"El dado {die_value} no está disponible en este turno."

        # Validaciones básicas de rango
        if not (1 <= start <= 24 and 1 <= end <= 24):
            return False, "Las posiciones deben estar entre 1 y 24."

        current_player = self.get_current_player()
        player_id = current_player.get_id()

        # Intenta delegar en Board.move_checker si está implementado
        board = self.__board__
        if hasattr(board, "move_checker"):
            try:
                # move_checker debe validar propiedad de las fichas, capturas, barra, bearing off, etc.
                board.move_checker(start, end, player_id)
                self.consume_die(die_value)
                self.__history__.append({"action": "move", "player": current_player.get_name(), "from": start, "to": end, "die": die_value})
                return True, "Movimiento aplicado con éxito."
            except Exception as e:
                return False, f"Movimiento inválido: {e}"
        else:
            # Si Board no implementa move_checker, informamos claramente lo que hace falta.
            raise NotImplementedError(
                "Board.no implementa 'move_checker(start, end, player_id)'. "
                "Agregá ese método en core/board.py o adaptá la interfaz del tablero. "
                "Un ejemplo de implementación está en la documentación del proyecto."
            )

    # ---------------------- Fin de turno y verificación de victoria ----------------------
    def end_turn(self):
        """
        Finaliza el turno actual: consume cualquier estado restante, suma turnos, cambia jugador.
        """
        current = self.get_current_player()
        current.add_turn()
        self.__turn_dice_values__.clear()
        self.__is_double__ = False
        self.switch_turn()

    def check_winner(self) -> Optional[Player]:
        """
        Verifica si alguno de los jugadores cumplió la condición de victoria (bearing off == 15).
        Returns:
            Player si hay ganador, None si no.
        """
        for p in self.__players__:
            if p.has_won():
                return p
        return None

    # ---------------------- Guardado / carga (opcional Redis o JSON local) ----------------------
    def serialize_state(self) -> str:
        """
        Serializa el estado esencial del juego a JSON (para guardado en Redis o archivo).
        NOTA: serializa nombres, ids y estado básico. No intenta serializar objetos complejos.
        Returns:
            str: JSON con estado.
        """
        state = {
            "players": [
                {
                    "id": p.get_id(),
                    "name": p.get_name(),
                    "color": p.get_color(),
                    "checkers": p.get_checkers(),
                    "captured": p.get_captured(),
                    "borne_off": p.get_borne_off(),
                    "score": p.get_score(),
                    "turns": p.get_turns(),
                } for p in self.__players__
            ],
            "current_player_index": self.__current_player_index__,
            "turn_dice_values": self.__turn_dice_values__,
            "board_points": self.__board__.get_all_points(),  # Asume lista serializable
            "history": self.__history__,
            "game_started": self.__game_started__
        }
        return json.dumps(state)

    def load_state_from_json(self, json_str: str):
        """
        Carga un estado serializado (compatibilidad básica).
        Args:
            json_str (str): JSON producido por serialize_state.
        Raises:
            ValueError: si el JSON no contiene campos esperados.
        """
        data = json.loads(json_str)
        # validaciones básicas
        if "players" not in data or "board_points" not in data:
            raise ValueError("JSON de estado inválido.")
        # Restaurar players (simplemente reasignamos datos a players existentes si coincide id)
        for pl_data in data["players"]:
            for p in self.__players__:
                if p.get_id() == pl_data["id"]:
                    p.set_color(pl_data.get("color", p.get_color()))
                    # nota: atributos internos como checkers/captured/borne_off no tienen setters públicos
                    # A futuro: exponer métodos para restaurar estado desde Board/Player.
        # Restauración de tablero dejada como tarea: Board debería exponer método load_points(...)
        if hasattr(self.__board__, "load_points"):
            self.__board__.load_points(data["board_points"])
        else:
            # no podemos cargar automáticamente el tablero si no existe la API
            raise NotImplementedError("Board no implementa load_points(...). Agregar para restauración completa.")
        self.__current_player_index__ = data.get("current_player_index", 0)
        self.__turn_dice_values__ = data.get("turn_dice_values", [])
        self.__history__ = data.get("history", [])
        self.__game_started__ = bool(data.get("game_started", False))

    # ---------------------- Utilidades ----------------------
    def game_summary(self) -> str:
        """
        Devuelve un resumen legible del estado actual del juego (para CLI / logs).
        """
        lines = []
        lines.append("=== Backgammon - Estado de la partida ===")
        for p in self.__players__:
            lines.append(str(p))
        lines.append(f"Turno actual: {self.get_current_player().get_name()}")
        lines.append(f"Dados disponibles: {self.__turn_dice_values__}")
        lines.append("=========================================")
        return "\n".join(lines)


