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
    PAUSED = 2
    EDITOR = 3


@dataclass
class Game:
    main: Main
    canvas: pygame.Surface

    mode: mode = field(init=False, default=mode.MENU)
    board: dict[tuple[int, int], tile] = field(init=False, default_factory=dict)

    selected: tile = field(init=False, default=None)

    font_30: pygame.font.Font = field(init=False)
    font_42: pygame.font.Font = field(init=False)
    font_60: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.font_30 = pygame.font.Font('assets/jetbrainsmononerd.ttf', 30)
        self.font_42 = pygame.font.Font('assets/jetbrainsmononerd.ttf', 42)
        self.font_60 = pygame.font.Font('assets/jetbrainsmononerd.ttf', 60)

    @property
    def start_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - TITLE_W, 250 - TITLE_H, 2 * TITLE_W, 2 * TITLE_H)

    def main_menu(self) -> None:

        clear_canvas(self.canvas)
        # title
        draw_centered_text(self.canvas, self.font_60.render('OpenPipe', True, 0xff55ffff),
                           self.main.x_center, 90)
        # difficulty buttons
        draw.rect(self.canvas, 0x00aa00, self.start_rect)
        draw_centered_text(self.canvas, self.font_42.render('Start', True, 0xffffffff),
                           self.main.x_center, 250)

    def update_board(self):
        for i in self.board:
            self.board[i].hit_box = draw.rect(self.canvas, self.board[i].color, pygame.Rect(100 + 50 * i[0], 100 + 50 * i[1], 50, 50), False)
            if self.board[i].strict:
                draw_centered_text(self.canvas, self.font_30.render('X', True, 0x000000), 125 + 50 * i[0], 125 + 50 * i[1])

    def draw_board(self, level: int) -> None:
        # generate board
        for i in LEVELS[level]['nodes']:
            self.board[i.coord] = tile(i.color)
        for i in range(LEVELS[level]['size']):
            for j in range(LEVELS[level]['size']):
                if (i, j) in self.board:
                    continue
                self.board[(i, j)] = tile(filled=False, strict=False)
        self.update_board()

    def run_game(self, level: int) -> None:
        self.mode = mode.PLAYING
        self.draw_board(level)
        clear_canvas(self.canvas)
        self.update_board()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.mode == mode.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_rect.collidepoint(mouse_pos):
                    self.run_game(1)

        if self.mode == mode.PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, j in self.board:
                    t1 = self.board[(i, j)]
                    if t1.hit_box.collidepoint(mouse_pos) and not self.selected and t1.color != color.gray and not t1.clicked:
                        self.selected = self.board[(i, j)]
                        print(self.board[(i, j)])

            if self.selected and event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                select_color = self.selected.color
                for i, j in self.board:
                    t1 = self.board[(i, j)]
                    if t1.hit_box.collidepoint(mouse_pos):
                        is_color_nearby = any([b.color == select_color for b in get_nearby(self.board, i, j)])
                        if t1.strict and is_color_nearby and t1 != self.selected and t1.color == select_color:
                            self.selected.clicked = True
                            self.selected = None
                            t1.clicked = True
                        if t1.strict:
                            continue
                        if is_color_nearby:
                            t1.color = select_color
                            t1.filled = True
            self.update_board()
