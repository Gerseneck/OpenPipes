from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import ClassVar, TYPE_CHECKING

import pygame.mouse
from pygame import draw

if TYPE_CHECKING:
    from main import Main

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


@dataclass
class Game:
    main: Main
    canvas: pygame.Surface

    mode: mode = field(init=False, default=mode.MENU)
    board: dict[tuple[int, int], tile] = field(init=False, default_factory=dict)

    level: int = field(init=False, default=0)
    level_name: str = field(init=False)
    level_size: int = field(init=False)
    level_nodes: list[node] = field(init=False)
    selected: tile = field(init=False, default=None)
    connected: int = field(init=False, default=0)
    required: int = field(init=False)

    time_start: int = field(init=False)
    time_end: int = field(init=False)

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
    def factor(self) -> int:
        return self.main.x_size // 800

    @property
    def start_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - TITLE_W, 250 - TITLE_H, 2 * TITLE_W, 2 * TITLE_H)

    @property
    def level_editor(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - TITLE_W, 250 - TITLE_H, 2 * TITLE_W, 2 * TITLE_H)

    @property
    def next_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - 90 - RESULT_W, self.main.y_size - 50 - RESULT_H, 2 * RESULT_W, 2 * RESULT_H)

    @property
    def menu_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center + 90 - RESULT_W, self.main.y_size - 50 - RESULT_H, 2 * RESULT_W, 2 * RESULT_H)

    def main_menu(self) -> None:
        self.mode = mode.MENU
        clear_canvas(self.canvas)
        draw_centered_text(self.canvas, self.font_60.render('OpenPipe', True, 0xff55ffff),
                           self.main.x_center, 90)
        draw.rect(self.canvas, 0x00aa00, self.start_rect)
        draw_centered_text(self.canvas, self.font_42.render('Start', True, 0xffffffff),
                           self.main.x_center, 250)

    def _update_board(self):
        if self.mode == mode.WIN:
            draw_centered_text(self.canvas, self.font_42.render('PERFECT!', True, 0xff55ffff),
                               self.main.x_center, 50)
            if self.level + 1 in LEVELS:
                draw.rect(self.canvas, 0x00aa00, self.next_rect)
                draw_centered_text(self.canvas, self.font_24.render('Next Level', True, 0xffffffff), self.main.x_center-90,
                                   self.main.y_size-50)
            draw.rect(self.canvas, 0x00aa00, self.menu_rect)
            draw_centered_text(self.canvas, self.font_24.render('Main Menu', True, 0xffffffff), self.main.x_center+90,
                               self.main.y_size-50)

        self.canvas.blit(self.font_30.render(self.level_name, True, 0x11ff11ff), (5, 5))
        self.canvas.blit(self.font_24.render(f'{self.connected}/{self.required} Connected', True, 0x11ff11ff), (7, 45))

        ticks_passed = self.main.number_tick - self.time_start if self.mode == mode.PLAYING else self.time_end - self.time_start
        seconds = ticks_passed // self.main.TPS
        time_text = f'\uf64f {seconds // 60:02d}:{seconds % 60:02d}'
        draw_right_align_text(self.canvas, self.font_24.render(time_text, True, 0x5555ffff), self.main.x_size - 5, 5)

        box_size = 350 * self.factor // self.level_size

        x_start = self.main.x_center - (self.level_size * box_size) // 2
        y_start = self.main.y_center - (self.level_size * box_size) // 2 + 15

        draw.rect(self.canvas, 0xffffff, pygame.Rect(x_start - 5, y_start - 5, self.level_size * box_size + 10, self.level_size * box_size + 10), 5)

        for i in self.board:
            self.board[i].hit_box = draw.rect(self.canvas, self.board[i].color,
                                              pygame.Rect(x_start + box_size * i[0], y_start + box_size * i[1], box_size, box_size), False)
            if self.board[i].strict:
                draw_centered_text(self.canvas, self.font_30.render('\u2713' if self.board[i].connected else 'X', True, 0x000000),
                                   x_start + box_size // 2 + box_size * i[0], y_start + box_size // 2 + box_size * i[1])

    def _create_board(self) -> None:
        # generate board
        for i in self.level_nodes:
            self.board[i.coord] = tile(*i.coord, color=i.color)
        for i in range(self.level_size):
            for j in range(self.level_size):
                if (i, j) in self.board:
                    continue
                self.board[(i, j)] = tile(i, j, filled=False, strict=False)
        self._update_board()

    def _clear_board(self):
        self.board = dict()
        self.selected = None
        self.connected = 0

    def run_game(self, level: int) -> None:
        self._clear_board()

        self.mode = mode.PLAYING
        self.level = level
        self.level_name = LEVELS[level]['name']
        self.level_size = LEVELS[level]['size']
        self.level_nodes = LEVELS[level]['nodes']
        self.required = len(LEVELS[level]['nodes']) // 2
        self.time_start = self.main.number_tick

        self._create_board()
        clear_canvas(self.canvas)
        self._update_board()

    def tick_loop(self) -> None:
        if self.mode == mode.MENU:
            clear_canvas(self.canvas)
            self.main_menu()
        if self.mode == mode.PLAYING or self.mode == mode.WIN:
            self.connected = check_number_connected(self.board)
            clear_canvas(self.canvas)
            self._update_board()

            if pygame.key.get_pressed()[pygame.K_r]:
                clear_canvas(self.canvas)
                self.run_game(self.level)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.mode == mode.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_rect.collidepoint(mouse_pos):
                    self.run_game(0)

        if self.mode == mode.WIN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.next_rect.collidepoint(mouse_pos) and self.level + 1 in LEVELS:
                    self.run_game(self.level + 1)
                if self.menu_rect.collidepoint(mouse_pos):
                    self.main_menu()

        if self.mode == mode.PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, j in self.board:
                    t1 = self.board[(i, j)]
                    if t1.hit_box.collidepoint(mouse_pos) and t1.strict and t1.color != color.gray:
                        if t1.connected:
                            clear_color(self.board, t1.color)
                            continue
                        self.selected = self.board[(i, j)]

            if self.selected and event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                select_color = self.selected.color
                for i, j in self.board:
                    t1 = self.board[(i, j)]
                    if t1.hit_box.collidepoint(mouse_pos):
                        is_color_nearby = any([b.color == select_color for b in get_nearby(self.board, i, j) if (
                                b.strict and b == self.selected) or not b.strict])  ## check if the color is nearby and able to connect
                        if t1.strict and is_color_nearby and t1 != self.selected and t1.color == select_color:
                            self.selected.connected = True
                            self.selected = None
                            self.connected += 1
                            t1.connected = True
                            if self.connected == self.required and check_filled(self.board):
                                self.mode = mode.WIN
                                self.time_end = self.main.number_tick
                            continue
                        if t1.strict:
                            continue
                        if is_color_nearby:
                            if t1.filled and t1.color != select_color:
                                clear_color(self.board, t1.color)
                            t1.color = select_color
                            t1.filled = True


