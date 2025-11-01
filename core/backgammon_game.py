# core/backgammon_game.py
import random
from .board import Board, WHITE, BLACK
from .dice import Dice
from .player import Player

class BackgammonGame:
    def __init__(self, rng=None):
        self.__rng__ = rng or random.Random()
        self.__board__ = Board()
        self.__current_player__ = WHITE
        self.__dice__ = Dice(rng)
        self.__players__ = {
            WHITE: Player("Jugador Blanco", WHITE),
            BLACK: Player("Jugador Negro", BLACK)
        }

    # --- Propiedades (compatibles con pygame_ui) ---
    @property
    def points(self):
        return self.__board__.__points__

    @property
    def bar(self):
        return self.__board__.__bar__

    @property
    def borne_off(self):
        return self.__board__.__borne_off__

    @property
    def remaining_moves(self):
        """Devuelve los valores de movimiento disponibles (dados activos)."""
        return self.__dice__.values
    
    # ----------------------------------------------------------
    # Utilidades / proxies
    # ----------------------------------------------------------
    def opponent(self, player):
        return self.__board__.opponent(player)

    def direction(self, player):
        return self.__board__.direction(player)

    def home_range(self, player):
        return self.__board__.home_range(player)

    def _dest_index(self, player, from_idx, die):
        return self.__board__.dest_index(player, from_idx, die)

    def _point_is_blocked(self, player, idx):
        return self.__board__.point_is_blocked(player, idx)

    # ----------------------------------------------------------
    # Dados / turno
    # ----------------------------------------------------------
    def roll_dice(self):
        """Tira los dados usando la clase Dice."""
        self.__dice__.roll()
        return tuple(self.__dice__.values)

    def consume_move(self, die):
        """Consume un valor del dado."""
        self.__dice__.consume(die)

    # ----------------------------------------------------------
    # Flujo del juego
    # ----------------------------------------------------------
    def switch_turn(self):
        """Cambia el turno al jugador oponente."""
        self.__current_player__ = self.opponent(self.__current_player__)
        self.__dice__.reset()

    def current_player_obj(self):
        """Devuelve el objeto Player del jugador actual."""
        return self.__players__[self.__current_player__]

    def reset(self):
        """Reinicia el estado del juego."""
        self.__board__.reset()
        self.__dice__.reset()
        for player in self.__players__.values():
            player.reset()
        self.__current_player__ = WHITE

    # ----------------------------------------------------------
    # Lógica de movimientos (proxies + helpers)
    # ----------------------------------------------------------
    def combined_move_destination(self, player, from_idx, dice_list):
        """Calcula destino si se combinan los dos primeros dados."""
        if len(dice_list) < 2:
            return None

        #  Solo tomar los dos primeros valores únicos
        dice_unique = sorted(set(dice_list))
        if len(dice_unique) < 2:
            return None

        d1, d2 = dice_unique[:2]
        dirn = self.direction(player)
        mid_idx = from_idx + dirn * d1
        dest_idx = from_idx + dirn * (d1 + d2)

        if not (0 <= mid_idx <= 23 and 0 <= dest_idx <= 23):
            return None
        if self._point_is_blocked(player, mid_idx):
            return None
        if self._point_is_blocked(player, dest_idx):
            return None
        return dest_idx


    def try_combined_move(self, from_idx, dice_list):
        if len(dice_list) < 2:
            return False
        d1, d2 = sorted(dice_list)
        dirn = self.direction(self.__current_player__)
        mid_idx = from_idx + dirn * d1
        dest_idx = from_idx + dirn * (d1 + d2)
        if not (0 <= mid_idx <= 23 and 0 <= dest_idx <= 23):
            return False
        if self._point_is_blocked(self.__current_player__, mid_idx):
            return False
        if self._point_is_blocked(self.__current_player__, dest_idx):
            return False
        if not self.__board__.move_checker(self.__current_player__, from_idx, d1):
            return False
        if not self.__board__.move_checker(self.__current_player__, mid_idx, d2):
            owner, cnt = self.points[mid_idx]
            if owner == self.__current_player__ and cnt > 0:
                self.points[mid_idx] = (0, 0)
                self.points[from_idx] = (self.__current_player__, 1)
            return False
        self.consume_move(d1)
        self.consume_move(d2)
        return True

    def bearing_off_allowed(self, player):
        return self.__board__.bearing_off_allowed(player)

    def can_bear_off(self, player):
        return self.__board__.can_bear_off(player)

    def try_bear_off(self, from_idx, die):
        if die not in self.remaining_moves:
            return False
        if not self.__board__.can_bear_off_with_die(self.__current_player__, die):
            return False
        ok = self.__board__.move_checker(self.__current_player__, from_idx, die)
        if ok:
            self.consume_move(die)
        return ok

    def try_bear_off_click(self, from_idx):
        owner, cnt = self.points[from_idx]
        if owner != self.__current_player__ or cnt == 0:
            return False
        if not self.bearing_off_allowed(self.__current_player__):
            return False
        if from_idx not in self.home_range(self.__current_player__):
            return False
        need = self.__board__.distance_to_bear_off(self.__current_player__, from_idx)
        if need in self.remaining_moves:
            if self.__board__.move_checker(self.__current_player__, from_idx, need):
                self.consume_move(need)
                return True
        for die in sorted(set(self.remaining_moves)):
            if die > need and self.__board__.can_bear_off_with_die(self.__current_player__, die):
                if self.__board__.move_checker(self.__current_player__, from_idx, die):
                    self.consume_move(die)
                    return True
        return False

    def legal_single_sources(self, player, die):
        res = set()
        if self.bar[player] > 0:
            idx = self.__board__.enter_from_bar_targets(player, die)[0]
            if not self._point_is_blocked(player, idx):
                res.add(None)
            return sorted(res, key=lambda x: -1 if x is None else x)
        for i in range(24):
            owner, cnt = self.points[i]
            if owner == player and cnt > 0:
                dest = self._dest_index(player, i, die)
                if 0 <= dest <= 23 and not self._point_is_blocked(player, dest):
                    res.add(i)
                elif self.__board__.can_bear_off_with_die(player, die):
                    res.add(i)
        return sorted(res)

    def any_move_available(self, player, dice_list):
        for d in dice_list:
            if self.legal_single_sources(player, d):
                return True
        return False

    

    def try_move(self, from_idx, die):
        if die not in self.remaining_moves:
            return False
        ok = self.__board__.move_checker(self.__current_player__, from_idx, die)
        if ok:
            self.consume_move(die)
        return ok

    # ----------------------------------------------------------
    # Flujo de juego
    # ----------------------------------------------------------
    def end_turn_if_needed(self):
        if not self.remaining_moves or not self.any_move_available(self.__current_player__, self.remaining_moves):
            self.__current_player__ = self.opponent(self.__current_player__)
            self.roll_dice()

    def start_game_turn(self):
        if not self.remaining_moves:
            self.roll_dice()

    def is_game_over(self):
        return self.borne_off[WHITE] == 15 or self.borne_off[BLACK] == 15

    def winner(self):
        if self.borne_off[WHITE] == 15:
            return WHITE
        if self.borne_off[BLACK] == 15:
            return BLACK
        return 0