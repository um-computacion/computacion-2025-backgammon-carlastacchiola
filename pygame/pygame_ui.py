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
        self.__screen__ = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Backgammon - Carla Edition ")
        self.__clock__ = pygame.time.Clock()
        self.__font__ = pygame.font.SysFont(None, 28)

        self.__game__ = BackgammonGame()
        self.__await_roll__ = True
        self.__selected_from__ = None
        self.__message__ = "Presiona ESPACIO para tirar los dados"

        # zonas de borne off (a la derecha)
        self.__off_white_rect__ = pygame.Rect(
            BOARD_W + 5, PADDING, EXTRA_W - 10, (HEIGHT - 2 * PADDING) // 2 - 10
        )
        self.__off_black_rect__ = pygame.Rect(
            BOARD_W + 5, HEIGHT // 2 + 10, EXTRA_W - 10, (HEIGHT - 2 * PADDING) // 2 - 10
        )

    # ----------------------------------------------------------
    def draw_board(self, legal_from, highlight_points):
        s = self.__screen__
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
            owner, cnt = self.__game__.points[i]
            if cnt > 0:
                col, side = idx_to_col_side(i)
                x = point_x(col) + POINT_W // 2
                color = WHITE_CHK if owner == WHITE else BLACK_CHK
                for k in range(cnt):
                    y = (BOARD_TOP + 20 + k * 26) if side == "top" else (BOARD_BOT - 20 - k * 26)
                    draw_disc(color, int(x), int(y))

        # fichas en barra
        bar_x = PADDING + 6 * POINT_W + BAR_W // 2
        for k in range(self.__game__.bar[WHITE]):
            y = HEIGHT // 2 - 50 - k * 28
            draw_disc(WHITE_CHK, bar_x, y)
        for k in range(self.__game__.bar[BLACK]):
            y = HEIGHT // 2 + 50 + k * 28
            draw_disc(BLACK_CHK, bar_x, y)

        # borne off áreas
        pygame.draw.rect(s, (90, 45, 20), self.__off_white_rect__, border_radius=10)
        pygame.draw.rect(s, (90, 45, 20), self.__off_black_rect__, border_radius=10)

        for k in range(self.__game__.borne_off[WHITE]):
            draw_disc(WHITE_CHK, self.__off_white_rect__.centerx, self.__off_white_rect__.top + 25 + k * 22)
        for k in range(self.__game__.borne_off[BLACK]):
            draw_disc(BLACK_CHK, self.__off_black_rect__.centerx, self.__off_black_rect__.top + 25 + k * 22)

        dice_txt = self.__font__.render(f"Dados: {self.__game__.__dice__.values}", True, TEXT_COLOR)
        s.blit(dice_txt, (20, 10))
        msg_txt = self.__font__.render(self.__message__, True, TEXT_COLOR)
        s.blit(msg_txt, (WIDTH // 2 - msg_txt.get_width() // 2, 10))
        cnt_txt = self.__font__.render(
            f"Fichas fuera 🡒 Blanco: {self.__game__.borne_off[WHITE]} | Negro: {self.__game__.borne_off[BLACK]}",
            True, TEXT_COLOR
        )
        s.blit(cnt_txt, (WIDTH // 2 - cnt_txt.get_width() // 2, HEIGHT - 30))

    # ----------------------------------------------------------
    def run(self):
        running = True
        while running:
            legal_sources = set()
            highlight_points = []

            if not self.__await_roll__:
                for d in sorted(set(self.__game__.__dice__.values)):
                    legal_sources.update(self.__game__.legal_single_sources(self.__game__.__current_player__, d))

                if self.__selected_from__ is None and self.__game__.bar[self.__game__.__current_player__] > 0:
                    # desde la barra: destinos de entrada
                    for die in sorted(set(self.__game__.__dice__.values)):
                        targets = self.__game__.__board__.enter_from_bar_targets(self.__game__.__current_player__, die)
                        for t in targets:
                            if not self.__game__._point_is_blocked(self.__game__.__current_player__, t):
                                highlight_points.append(t)

                elif self.__selected_from__ is not None:
                    # normales: destinos por cada dado
                    for die in sorted(set(self.__game__.__dice__.values)):
                        dest = self.__game__._dest_index(self.__game__.__current_player__, self.__selected_from__, die)
                        if 0 <= dest <= 23 and not self.__game__._point_is_blocked(self.__game__.__current_player__, dest):
                            highlight_points.append(dest)

                    # destino combinado (a + b)
                    if len(self.__game__.__dice__.values) >= 2:
                        combo_dest = self.__game__.combined_move_destination(
                            self.__game__.__current_player__,
                            self.__selected_from__,
                            list(self.__game__.__dice__.values)[:2]
                        )
                        if combo_dest is not None and 0 <= combo_dest <= 23:
                            highlight_points.append(combo_dest)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.__await_roll__:
                        self.__game__.roll_dice()
                        self.__await_roll__ = False
                        self.__message__ = "Haz clic en una ficha válida"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if self.__await_roll__:
                        continue

                    # clic en barra
                    if clicked_on_bar(x, y) and self.__game__.bar[self.__game__.__current_player__] > 0:
                        self.__selected_from__ = None
                        self.__message__ = "Seleccionada ficha desde la barra"
                        continue

                    if self.__game__.__current_player__ == WHITE and self.__off_white_rect__.collidepoint(x, y):
                            if self.__selected_from__ is not None and self.__game__.try_bear_off_click(self.__selected_from__):
                                self.__message__ = "Ficha borne off "
                                self.__selected_from__ = None
                            else:
                                self.__message__ = "No puedes sacar esa ficha todavía"
                            continue

                    if self.__game__.__current_player__ == BLACK and self.__off_black_rect__.collidepoint(x, y):
                            if self.__selected_from__ is not None and self.__game__.try_bear_off_click(self.__selected_from__):
                                self.__message__ = "Ficha borne off "
                                self.__selected_from__ = None
                            else:
                                self.__message__ = "No puedes sacar esa ficha todavía"
                            continue

                    idx = point_index_from_xy(x, y)
                    moved = False

                    if self.__selected_from__ is None and self.__game__.bar[self.__game__.__current_player__] > 0:
                        # movimiento desde barra
                        for die in sorted(set(self.__game__.__dice__.values), reverse=True):
                            targets = self.__game__.__board__.enter_from_bar_targets(self.__game__.__current_player__, die)
                            if targets and targets[0] == idx:
                                if self.__game__.try_move(None, die):
                                    moved = True
                                    break
                        if moved:
                            self.__message__ = "Ficha reingresada al tablero"
                            self.__selected_from__ = None
                        else:
                            self.__message__ = "No se puede mover desde la barra aquí"
                        continue

                    if self.__selected_from__ is None:
                        if idx in legal_sources:
                            self.__selected_from__ = idx
                            self.__message__ = f"Seleccionado punto {idx + 1}"
                        else:
                            self.__message__ = "Haz clic en una ficha válida"
                    else:
                        moved = False

                        # 1 primero: intentar movimiento combinado (a+b)
                        if len(self.__game__.__dice__.values) >= 2:
                            combo_dest = self.__game__.combined_move_destination(
                                self.__game__.current_player,
                                self.__selected_from__,
                                list(self.__game__.dice.values)[:2]   # usamos los 2 dados del turno
                            )
                            if combo_dest == idx:
                                if self.__game__.try_combined_move(self.__selected_from__, list(self.__game__.__dice__.values)[:2]):
                                    moved = True

                        # 2 si NO fue combinado, intentar movimientos simples
                        if not moved:
                            for die in sorted(set(self.__game__.__dice__.values), reverse=True):
                                dest = self.__game__._dest_index(self.__game__.__current_player__, self.__selected_from__, die)
                                if dest == idx and self.__game__.try_move(self.__selected_from__, die):
                                    moved = True
                                    break

                        # 3 si se movió: mensaje + chequeo de fin de turno
                        if moved:
                            self.__message__ = "Movimiento OK"
                            self.__selected_from__ = None
                            # si ya no quedan movimientos o no hay jugadas, cambiar turno
                            if self.__game__.__dice__.is_empty() or not self.__game__.any_move_available(
                                self.__game__.__current_player__, self.__game__.__dice__.values
                            ):
                                self.__game__.switch_turn()
                                self.__await_roll__ = True
                                self.__message__ = "Presiona ESPACIO para tirar los dados"
                        else:
                            # 4 no se movió: quizá hizo clic en OTRA ficha suya → cambiar selección
                            if idx is not None and idx in legal_sources:
                                self.__selected_from__ = idx
                                self.__message__ = f"Seleccionado punto {idx + 1}"
                            else:
                                moved = False

                                # clic en rectángulo de borne off (sacar ficha seleccionada)
                                if self.__selected_from__ is not None:
                                    if self.__game__.__current_player__ == WHITE and self.__off_white_rect__.collidepoint(x, y):
                                        moved = self.__game__.try_bear_off_click(self.__selected_from__)
                                    elif self.__game__.__current_player__ == BLACK and self.__off_black_rect__.collidepoint(x, y):
                                        moved = self.__game__.try_bear_off_click(self.__selected_from__)

                                    if moved:
                                        self.__message__ = "Ficha fuera del tablero"
                                        self._selected_from__ = None
                                        if self.__game__.__dice__.is_empty() or not self.__game__.any_move_available(
                                            self.__game__.__current_player__, self.__game__.__dice__.values
                                        ):
                                            self.__game__.switch_turn()
                                            self.__await_roll__ = True
                                            self.__message__ = "Presiona ESPACIO para tirar los dados"
                                        continue
                                    else:
                                        self.__message__ = "No se puede sacar con estos dados"
                                        self.__selected_from__ = None
                                        continue

                                # 🧱 si no fue borne-off, ni otro tipo de movimiento válido:
                                self.__selected_from__ = None
                                self.__message__ = "Movimiento no permitido"



            self.draw_board([i for i in legal_sources if i is not None], highlight_points)
            pygame.display.flip()
            self.__clock__.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ui = PygameUI()
    ui.run()
