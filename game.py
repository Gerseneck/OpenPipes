from __future__ import annotations

import enum
from typing import TYPE_CHECKING

import pygame.mouse
from pygame import draw

if TYPE_CHECKING:
    from main import Main

from core import Core
from editor import Editor
from util import *
from data.level import LEVELS

TITLE_W = 270
TITLE_H = 35
RESULT_W = 85
RESULT_H = 20


class mode(enum.Enum):
    MENU = 0
    PLAYING = 1
    WIN = 2
    EDITOR = 3
    LOAD = 4


@dataclass
class Game:
    main: Main
    canvas: pygame.Surface

    core: Core = field(init=False, default=None)
    editor: Editor = field(init=False, default=None)

    mode: mode = field(init=False, default=mode.MENU)

    font_24: pygame.font.Font = field(init=False)
    font_30: pygame.font.Font = field(init=False)
    font_42: pygame.font.Font = field(init=False)
    font_60: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.font_24 = pygame.font.Font('assets/jetbrainsmononerd.ttf', 24)
        self.font_30 = pygame.font.Font('assets/jetbrainsmononerd.ttf', 30)
        self.font_42 = pygame.font.Font('assets/jetbrainsmononerd.ttf', 42)
        self.font_60 = pygame.font.Font('assets/jetbrainsmononerd.ttf', 60)

    @property
    def start_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - TITLE_W, 250 - TITLE_H, 2 * TITLE_W, 2 * TITLE_H)

    @property
    def level_editor(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - TITLE_W, 350 - TITLE_H, 2 * TITLE_W, 2 * TITLE_H)

    @property
    def load_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - TITLE_W, 450 - TITLE_H, TITLE_W,
                           2 * TITLE_H)

    @property
    def next_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - 90 - RESULT_W, self.main.y_size - 50 - RESULT_H, 2 * RESULT_W,
                           2 * RESULT_H)

    @property
    def menu_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center + 90 - RESULT_W, self.main.y_size - 50 - RESULT_H, 2 * RESULT_W,
                           2 * RESULT_H)

    def main_menu(self) -> None:
        self.mode = mode.MENU
        clear_canvas(self.canvas)
        draw_centered_text(self.canvas, self.font_60.render('OpenPipe', True, 0xff55ffff),
                           self.main.x_center, 90)
        draw.rect(self.canvas, 0x00aa00, self.start_rect)
        draw_centered_text(self.canvas, self.font_42.render('Start', True, 0xffffffff),
                           self.main.x_center, 250)
        draw.rect(self.canvas, 0x00aa00, self.level_editor)
        draw_centered_text(self.canvas, self.font_42.render('Level Editor', True, 0xffffffff),
                           self.main.x_center, 350)
        draw.rect(self.canvas, 0x00aa00, self.load_rect)
        draw_centered_text(self.canvas, self.font_42.render('Load Level', True, 0xffffffff),
                           self.main.x_center - TITLE_W // 2, 450)

    def _update_board(self):
        if self.mode == mode.MENU:
            self.main_menu()
            self.core = None
            self.editor = None
            return

        if self.mode == mode.EDITOR:
            self.editor.draw()
            draw.rect(self.canvas, 0x00aa00, self.next_rect)
            draw_centered_text(self.canvas, self.font_24.render('Save', True, 0xffffffff),
                               self.main.x_center - 90, self.main.y_size - 50)

        if self.mode != mode.EDITOR and self.core is not None:
            self.canvas.blit(self.font_24.render(f'{self.core.connected}/{self.core.required} Connected', True, 0x11ff11ff),
                             (7, 45))
            ticks_passed = self.main.number_tick - self.core.time_start if self.mode == mode.PLAYING else self.core.time_end - self.core.time_start
            seconds = ticks_passed // self.main.TPS
            time_text = f'\uf64f {seconds // 60:02d}:{seconds % 60:02d}'
            draw_right_align_text(self.canvas, self.font_24.render(time_text, True, 0x5555ffff), self.main.x_size - 5, 5)

        if self.mode == mode.WIN:
            draw_centered_text(self.canvas, self.font_42.render('PERFECT!', True, 0xff55ffff),
                               self.main.x_center, 50)
            if self.core.level + 1 in LEVELS:
                draw.rect(self.canvas, 0x00aa00, self.next_rect)
                draw_centered_text(self.canvas, self.font_24.render('Next Level', True, 0xffffffff),
                                   self.main.x_center - 90, self.main.y_size - 50)

        self.canvas.blit(self.font_30.render('Level editor' if self.core is None else self.core.level_name, True, 0x11ff11ff), (5, 5))
        draw.rect(self.canvas, 0x00aa00, self.menu_rect)
        draw_centered_text(self.canvas, self.font_24.render('Main Menu', True, 0xffffffff), self.main.x_center + 90,
                           self.main.y_size - 50)

        if self.core is not None:
            self.core.draw()

    def run_game(self, level: int) -> None:
        self.core = Core(self.main, self.canvas)
        self.core.run_game(level)
        self.mode = mode.PLAYING

    def run_level_editor(self) -> None:
        self.editor = Editor(self.main, self.canvas)
        self.editor.run()
        self.mode = mode.EDITOR

    def tick_loop(self) -> None:
        if self.mode == mode.PLAYING or self.mode == mode.WIN:
            self.core.connected = check_number_connected(self.core.board)

            if pygame.key.get_pressed()[pygame.K_r]:
                clear_canvas(self.canvas)
                self.run_game(self.core.level)

        clear_canvas(self.canvas)
        self._update_board()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.mode == mode.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_rect.collidepoint(mouse_pos):
                    self.run_game(0)
                if self.level_editor.collidepoint(mouse_pos):
                    self.run_level_editor()

        if self.mode == mode.EDITOR:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.menu_rect.collidepoint(mouse_pos):
                    self.main_menu()
                if self.next_rect.collidepoint(mouse_pos):
                    encode_data(self.editor.board, self.editor.board_name, self.editor.board_size)
                    print(unload_data(encode_data(self.editor.board, self.editor.board_name, self.editor.board_size)))
            self.editor.handle_event(event)

        if self.mode == mode.WIN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.next_rect.collidepoint(mouse_pos) and self.core.level + 1 in LEVELS:
                    self.run_game(self.core.level + 1)
                if self.menu_rect.collidepoint(mouse_pos):
                    self.main_menu()

        if self.mode == mode.PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.menu_rect.collidepoint(mouse_pos):
                    self.main_menu()

            if self.core.handle_event(event):
                self.mode = mode.WIN
                self.core.time_end = self.main.number_tick

