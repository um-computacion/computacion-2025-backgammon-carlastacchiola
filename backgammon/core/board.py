# backgammon/core/board.py

WHITE = 1
BLACK = -1


class Board:
    """
    Lógica pura del tablero de Backgammon:
    - points: lista de 24 tuplas (owner, count)
    - bar: fichas golpeadas por color
    - borne_off: fichas ya extraídas por color
    No conoce turnos ni tiradas: eso lo coordina BackgammonGame.
    """

    def __init__(self):
        self.points = [(0, 0)] * 24
        self.bar = {WHITE: 0, BLACK: 0}
        self.borne_off = {WHITE: 0, BLACK: 0}
        self.setup_initial()

    # ----------------------------------------------------------
    # Setup inicial
    # ----------------------------------------------------------
    def setup_initial(self):
        """Posición estándar del Backgammon."""
        self.points = [(0, 0)] * 24

        def set_point(num, owner, count):
            self.points[num - 1] = (owner, count)

        # Fichas blancas
        set_point(24, WHITE, 2)
        set_point(13, WHITE, 5)
        set_point(8, WHITE, 3)
        set_point(6, WHITE, 5)

        # Fichas negras
        set_point(1, BLACK, 2)
        set_point(12, BLACK, 5)
        set_point(17, BLACK, 3)
        set_point(19, BLACK, 5)

        self.bar = {WHITE: 0, BLACK: 0}
        self.borne_off = {WHITE: 0, BLACK: 0}

    # ----------------------------------------------------------
    # Utilidades básicas
    # ----------------------------------------------------------
    def opponent(self, player):
        return WHITE if player == BLACK else BLACK

    def direction(self, player):
        """Dirección de movimiento (WHITE hacia abajo, BLACK hacia arriba)."""
        return -1 if player == WHITE else 1

    def home_range(self, player):
        """Rango de índices del cuadrante propio."""
        return range(0, 6) if player == WHITE else range(18, 24)

    def dest_index(self, player, from_idx, die):
        """Calcula el índice destino según jugador y dado."""
        return from_idx + self.direction(player) * die

    def point_is_blocked(self, player, idx):
        """True si el punto está bloqueado por el oponente."""
        if idx < 0 or idx > 23:
            return False
        owner, count = self.points[idx]
        return owner == self.opponent(player) and count >= 2

    def enter_from_bar_targets(self, player, die):
        """Índice de entrada al tablero desde la barra."""
        return [24 - die] if player == WHITE else [die - 1]

    # ----------------------------------------------------------
    # Lógica de “bearing off” (sacar fichas)
    # ----------------------------------------------------------
    def bearing_off_allowed(self, player):
        """True si todas las fichas del jugador están dentro de su casa."""
        if self.bar[player] > 0:
            return False
        total_en_casa = 0
        for i in self.home_range(player):
            owner, count = self.points[i]
            if owner == player:
                total_en_casa += count
        return (total_en_casa + self.borne_off[player]) == 15

    def can_bear_off(self, player):
        """True si el jugador tiene todas sus fichas dentro del cuadrante de casa."""
        home = range(18, 24) if player == WHITE else range(0, 6)
        for idx, (owner, cnt) in enumerate(self.points):
            if owner == player and cnt > 0 and idx not in home:
                return False
        return True

    def can_bear_off_with_die(self, player, die):
        """Verifica si un jugador puede sacar ficha usando ese dado."""
        if not self.bearing_off_allowed(player):
            return False

        if player == WHITE:
            target_idx = die - 1
            owner, cnt = self.points[target_idx] if 0 <= target_idx <= 5 else (0, 0)
            if owner == WHITE and cnt > 0:
                return True
            for i in range(die, 6):
                o, c = self.points[i]
                if o == WHITE and c > 0:
                    return False
            for i in range(0, 6):
                o, c = self.points[i]
                if o == WHITE and c > 0:
                    return True
            return False
        else:
            target_idx = 24 - die
            owner, cnt = self.points[target_idx] if 18 <= target_idx <= 23 else (0, 0)
            if owner == BLACK and cnt > 0:
                return True
            for i in range(18, 24 - die):
                o, c = self.points[i]
                if o == BLACK and c > 0:
                    return False
            for i in range(18, 24):
                o, c = self.points[i]
                if o == BLACK and c > 0:
                    return True
            return False

    def distance_to_bear_off(self, player, from_idx):
        """Distancia que falta para sacar la ficha."""
        return (from_idx + 1) if player == WHITE else (24 - from_idx)

    def bear_off_piece(self, player, from_idx, search_range):
        """Elimina una ficha del tablero y la suma al borne_off."""
        owner, cnt = self.points[from_idx]
        if owner == player and cnt > 0:
            self.points[from_idx] = (0, 0) if cnt == 1 else (player, cnt - 1)
            self.borne_off[player] += 1
            return
        for i in search_range:
            o, c = self.points[i]
            if o == player and c > 0:
                self.points[i] = (0, 0) if c == 1 else (player, c - 1)
                self.borne_off[player] += 1
                break

    # ----------------------------------------------------------
    # Golpes y movimientos
    # ----------------------------------------------------------
    def apply_hit_if_any(self, player, idx):
        """Golpea una ficha del oponente si hay una sola."""
        owner, count = self.points[idx]
        if owner == self.opponent(player) and count == 1:
            self.bar[self.opponent(player)] += 1
            self.points[idx] = (0, 0)

    def move_checker(self, player, from_idx, die):
        """Movimiento atómico: desde un índice o desde la barra."""
        # --- Reingreso desde la barra ---
        if from_idx is None:
            dest = self.enter_from_bar_targets(player, die)[0]
            if self.point_is_blocked(player, dest):
                return False
            self.apply_hit_if_any(player, dest)
            owner, cnt = self.points[dest]
            if owner in (0, player):
                self.points[dest] = (player, cnt + 1)
                self.bar[player] -= 1
                return True
            return False

        # --- Movimiento normal ---
        dest = self.dest_index(player, from_idx, die)

        # Fuera del tablero → intentar bearing off
        if dest < 0 or dest > 23:
            if not self.can_bear_off_with_die(player, die):
                return False
            if player == WHITE:
                self.bear_off_piece(player, from_idx, range(5, -1, -1))
            else:
                self.bear_off_piece(player, from_idx, range(18, 24))
            return True

        # Punto bloqueado
        if self.point_is_blocked(player, dest):
            return False

        # Movimiento válido
        owner, cnt = self.points[from_idx]
        if owner != player or cnt == 0:
            return False

        self.apply_hit_if_any(player, dest)
        dest_owner, dest_cnt = self.points[dest]
        if dest_owner in (0, player):
            self.points[dest] = (player, dest_cnt + 1)
        else:
            self.points[dest] = (player, 1)

        remaining = cnt - 1
        self.points[from_idx] = (0, 0) if remaining == 0 else (player, remaining)
        return True

    # ----------------------------------------------------------
    # Reinicio
    # ----------------------------------------------------------
    def reset(self):
        """Reinicia el tablero al estado inicial."""
        self.setup_initial()