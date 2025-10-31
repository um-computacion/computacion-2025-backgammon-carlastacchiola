# backgammon/pygame/pygame_ui.py
import sys
import pygame
from core.backgammon_game import BackgammonGame, WHITE, BLACK

# --- CONFIG VISUAL ---
BOARD_W, BOARD_H = 1100, 700
EXTRA_W = 90
WIDTH, HEIGHT = BOARD_W + EXTRA_W, 700

GREEN_BG = (25, 70, 25)
WOOD_LIGHT = (218, 185, 140)
WOOD_DARK = (165, 120, 70)
POINT_LIGHT = (222, 180, 120)
POINT_DARK = (130, 90, 50)
WHITE_CHK = (250, 250, 250)
BLACK_CHK = (30, 30, 30)
HILITE = (90, 180, 255)
HILITE_MOVE = (100, 220, 100, 100)
TEXT_COLOR = (255, 255, 255)

PADDING = 40
BAR_W = 40
POINT_W = (BOARD_W - 2 * PADDING - BAR_W) // 12
BOARD_TOP = PADDING
BOARD_BOT = HEIGHT - PADDING


def point_x(col):
    if col <= 5:
        return PADDING + col * POINT_W
    else:
        return PADDING + BAR_W + (col - 6) * POINT_W + 6 * POINT_W


def idx_to_col_side(idx):
    p = idx + 1
    if p <= 12:
        col = 12 - p
        return col, "bottom"
    else:
        col = p - 13
        return col, "top"


def col_side_to_idx(col, side):
    if side == "bottom":
        p = 12 - col
    else:
        p = 13 + col
    return p - 1


def point_index_from_xy(x, y):
    if x < PADDING or x > BOARD_W - PADDING:
        return None

    if BOARD_TOP <= y <= BOARD_TOP + (BOARD_H - 2 * PADDING) // 2:
        side = "top"
    elif BOARD_BOT - (BOARD_H - 2 * PADDING) // 2 <= y <= BOARD_BOT:
        side = "bottom"
    else:
        return None

    for col in range(12):
        x0 = point_x(col)
        if x0 <= x <= x0 + POINT_W:
            return col_side_to_idx(col, side)
    return None


def clicked_on_bar(x, y):
    bx = PADDING + 6 * POINT_W
    return bx <= x <= bx + BAR_W and PADDING <= y <= PADDING + (HEIGHT - 2 * PADDING)


class PygameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Backgammon - Carla Edition ")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

        self.game = BackgammonGame()
        self.await_roll = True
        self.selected_from = None
        self.message = "Presiona ESPACIO para tirar los dados"

        # zonas de borne off (a la derecha)
        self.off_white_rect = pygame.Rect(
            BOARD_W + 5, PADDING, EXTRA_W - 10, (HEIGHT - 2 * PADDING) // 2 - 10
        )
        self.off_black_rect = pygame.Rect(
            BOARD_W + 5, HEIGHT // 2 + 10, EXTRA_W - 10, (HEIGHT - 2 * PADDING) // 2 - 10
        )

    # ----------------------------------------------------------
    def draw_board(self, legal_from, highlight_points):
        s = self.screen
        s.fill(GREEN_BG)

        # tablero base
        pygame.draw.rect(
            s, WOOD_LIGHT, (PADDING, PADDING, BOARD_W - 2 * PADDING, HEIGHT - 2 * PADDING), border_radius=8
        )

        bx = PADDING + 6 * POINT_W
        pygame.draw.rect(s, WOOD_DARK, (bx, PADDING, BAR_W, HEIGHT - 2 * PADDING))

        tri_h = (HEIGHT - 2 * PADDING) // 2
        for c in range(12):
            x = point_x(c)
            color = POINT_LIGHT if c % 2 == 0 else POINT_DARK
            pygame.draw.polygon(
                s, color, [(x, BOARD_TOP), (x + POINT_W, BOARD_TOP), (x + POINT_W / 2, BOARD_TOP + tri_h)]
            )
            pygame.draw.polygon(
                s, color, [(x, BOARD_BOT), (x + POINT_W, BOARD_BOT), (x + POINT_W / 2, BOARD_BOT - tri_h)]
            )

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for idx in highlight_points:
            col, side = idx_to_col_side(idx)
            x = point_x(col)
            if side == "top":
                pygame.draw.polygon(
                    overlay, HILITE_MOVE, [(x, BOARD_TOP), (x + POINT_W, BOARD_TOP), (x + POINT_W / 2, BOARD_TOP + tri_h)]
                )
            else:
                pygame.draw.polygon(
                    overlay, HILITE_MOVE, [(x, BOARD_BOT), (x + POINT_W, BOARD_BOT), (x + POINT_W / 2, BOARD_BOT - tri_h)]
                )
        s.blit(overlay, (0, 0))

        def draw_disc(color, x, y):
            pygame.draw.circle(s, (60, 60, 60), (x + 1, y + 1), 16)
            pygame.draw.circle(s, color, (x, y), 16)
            pygame.draw.circle(s, (100, 100, 100), (x, y), 16, 1)

        # fichas en puntos
        for i in range(24):
            owner, cnt = self.game.points[i]
            if cnt > 0:
                col, side = idx_to_col_side(i)
                x = point_x(col) + POINT_W // 2
                color = WHITE_CHK if owner == WHITE else BLACK_CHK
                for k in range(cnt):
                    y = (BOARD_TOP + 20 + k * 26) if side == "top" else (BOARD_BOT - 20 - k * 26)
                    draw_disc(color, int(x), int(y))

        # fichas en barra
        bar_x = PADDING + 6 * POINT_W + BAR_W // 2
        for k in range(self.game.bar[WHITE]):
            y = HEIGHT // 2 - 50 - k * 28
            draw_disc(WHITE_CHK, bar_x, y)
        for k in range(self.game.bar[BLACK]):
            y = HEIGHT // 2 + 50 + k * 28
            draw_disc(BLACK_CHK, bar_x, y)

        # borne off áreas
        pygame.draw.rect(s, (90, 45, 20), self.off_white_rect, border_radius=10)
        pygame.draw.rect(s, (90, 45, 20), self.off_black_rect, border_radius=10)

        for k in range(self.game.borne_off[WHITE]):
            draw_disc(WHITE_CHK, self.off_white_rect.centerx, self.off_white_rect.top + 25 + k * 22)
        for k in range(self.game.borne_off[BLACK]):
            draw_disc(BLACK_CHK, self.off_black_rect.centerx, self.off_black_rect.top + 25 + k * 22)

        dice_txt = self.font.render(f"Dados: {self.game.dice.values}", True, TEXT_COLOR)
        s.blit(dice_txt, (20, 10))
        msg_txt = self.font.render(self.message, True, TEXT_COLOR)
        s.blit(msg_txt, (WIDTH // 2 - msg_txt.get_width() // 2, 10))
        cnt_txt = self.font.render(
            f"Fichas fuera 🡒 Blanco: {self.game.borne_off[WHITE]} | Negro: {self.game.borne_off[BLACK]}",
            True, TEXT_COLOR
        )
        s.blit(cnt_txt, (WIDTH // 2 - cnt_txt.get_width() // 2, HEIGHT - 30))

    # ----------------------------------------------------------
    def run(self):
        running = True
        while running:
            legal_sources = set()
            highlight_points = []

            if not self.await_roll:
                for d in sorted(set(self.game.dice.values)):
                    legal_sources.update(self.game.legal_single_sources(self.game.current_player, d))

                if self.selected_from is None and self.game.bar[self.game.current_player] > 0:
                    # desde la barra: destinos de entrada
                    for die in sorted(set(self.game.dice.values)):
                        targets = self.game.board.enter_from_bar_targets(self.game.current_player, die)
                        for t in targets:
                            if not self.game._point_is_blocked(self.game.current_player, t):
                                highlight_points.append(t)

                elif self.selected_from is not None:
                    # normales: destinos por cada dado
                    for die in sorted(set(self.game.dice.values)):
                        dest = self.game._dest_index(self.game.current_player, self.selected_from, die)
                        if 0 <= dest <= 23 and not self.game._point_is_blocked(self.game.current_player, dest):
                            highlight_points.append(dest)

                    # destino combinado (a + b)
                    if len(self.game.dice.values) >= 2:
                        combo_dest = self.game.combined_move_destination(
                            self.game.current_player,
                            self.selected_from,
                            list(self.game.dice.values)[:2]
                        )
                        if combo_dest is not None and 0 <= combo_dest <= 23:
                            highlight_points.append(combo_dest)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.await_roll:
                        self.game.roll_dice()
                        self.await_roll = False
                        self.message = "Haz clic en una ficha válida"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if self.await_roll:
                        continue

                    # clic en barra
                    if clicked_on_bar(x, y) and self.game.bar[self.game.current_player] > 0:
                        self.selected_from = None
                        self.message = "Seleccionada ficha desde la barra"
                        continue

                    if self.game.current_player == WHITE and self.off_white_rect.collidepoint(x, y):
                            if self.selected_from is not None and self.game.try_bear_off_click(self.selected_from):
                                self.message = "Ficha borne off "
                                self.selected_from = None
                            else:
                                self.message = "No puedes sacar esa ficha todavía"
                            continue

                    if self.game.current_player == BLACK and self.off_black_rect.collidepoint(x, y):
                            if self.selected_from is not None and self.game.try_bear_off_click(self.selected_from):
                                self.message = "Ficha borne off "
                                self.selected_from = None
                            else:
                                self.message = "No puedes sacar esa ficha todavía"
                            continue

                    idx = point_index_from_xy(x, y)
                    moved = False

                    if self.selected_from is None and self.game.bar[self.game.current_player] > 0:
                        # movimiento desde barra
                        for die in sorted(set(self.game.dice.values), reverse=True):
                            targets = self.game.board.enter_from_bar_targets(self.game.current_player, die)
                            if targets and targets[0] == idx:
                                if self.game.try_move(None, die):
                                    moved = True
                                    break
                        if moved:
                            self.message = "Ficha reingresada al tablero"
                            self.selected_from = None
                        else:
                            self.message = "No se puede mover desde la barra aquí"
                        continue

                    if self.selected_from is None:
                        if idx in legal_sources:
                            self.selected_from = idx
                            self.message = f"Seleccionado punto {idx + 1}"
                        else:
                            self.message = "Haz clic en una ficha válida"
                    else:
                        moved = False

                        # 1 primero: intentar movimiento combinado (a+b)
                        if len(self.game.dice.values) >= 2:
                            combo_dest = self.game.combined_move_destination(
                                self.game.current_player,
                                self.selected_from,
                                list(self.game.dice.values)[:2]   # usamos los 2 dados del turno
                            )
                            if combo_dest == idx:
                                if self.game.try_combined_move(self.selected_from, list(self.game.dice.values)[:2]):
                                    moved = True

                        # 2 si NO fue combinado, intentar movimientos simples
                        if not moved:
                            for die in sorted(set(self.game.dice.values), reverse=True):
                                dest = self.game._dest_index(self.game.current_player, self.selected_from, die)
                                if dest == idx and self.game.try_move(self.selected_from, die):
                                    moved = True
                                    break

                        # 3 si se movió: mensaje + chequeo de fin de turno
                        if moved:
                            self.message = "Movimiento OK"
                            self.selected_from = None
                            # si ya no quedan movimientos o no hay jugadas, cambiar turno
                            if self.game.dice.is_empty() or not self.game.any_move_available(
                                self.game.current_player, self.game.dice.values
                            ):
                                self.game.switch_turn()
                                self.await_roll = True
                                self.message = "Presiona ESPACIO para tirar los dados"
                        else:
                            # 4 no se movió: quizá hizo clic en OTRA ficha suya → cambiar selección
                            if idx is not None and idx in legal_sources:
                                self.selected_from = idx
                                self.message = f"Seleccionado punto {idx + 1}"
                            else:
                                moved = False

                                # clic en rectángulo de borne off (sacar ficha seleccionada)
                                if self.selected_from is not None:
                                    if self.game.current_player == WHITE and self.off_white_rect.collidepoint(x, y):
                                        moved = self.game.try_bear_off_click(self.selected_from)
                                    elif self.game.current_player == BLACK and self.off_black_rect.collidepoint(x, y):
                                        moved = self.game.try_bear_off_click(self.selected_from)

                                    if moved:
                                        self.message = "Ficha fuera del tablero"
                                        self.selected_from = None
                                        if self.game.dice.is_empty() or not self.game.any_move_available(
                                            self.game.current_player, self.game.dice.values
                                        ):
                                            self.game.switch_turn()
                                            self.await_roll = True
                                            self.message = "Presiona ESPACIO para tirar los dados"
                                        continue
                                    else:
                                        self.message = "No se puede sacar con estos dados"
                                        self.selected_from = None
                                        continue

                                # 🧱 si no fue borne-off, ni otro tipo de movimiento válido:
                                self.selected_from = None
                                self.message = "Movimiento no permitido"



            self.draw_board([i for i in legal_sources if i is not None], highlight_points)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ui = PygameUI()
    ui.run()
