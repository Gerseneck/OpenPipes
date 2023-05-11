from __future__ import annotations

import enum
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame
from pygame import draw

if TYPE_CHECKING:
    from main import Main

from util import tile, draw_centered_text, clear_canvas


@dataclass
class Editor:
    main: Main
    canvas: pygame.Surface

    board: dict[tuple[int, int], tile] = field(init=False, default_factory=dict)
    board_size: int = field(init=False, default=5)

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

    def _update_board(self) -> None:
        box_size = 350 * self.factor // self.board_size
        x_start = self.main.x_center - (self.board_size * box_size) // 2
        y_start = self.main.y_center - (self.board_size * box_size) // 2 + 15

        draw.rect(self.canvas, 0xffffff, pygame.Rect(x_start - 5, y_start - 5, self.board_size * box_size + 10,
                                                     self.board_size * box_size + 10), 5)

        for i in self.board:
            self.board[i].hit_box = draw.rect(self.canvas, self.board[i].color,
                                              pygame.Rect(x_start + box_size * i[0], y_start + box_size * i[1],
                                                          box_size, box_size), False)
            if self.board[i].strict:
                draw_centered_text(self.canvas,
                                   self.font_30.render('X', True, 0x000000),
                                   x_start + box_size // 2 + box_size * i[0], y_start + box_size // 2 + box_size * i[1])

    def _clear_board(self) -> None:
        self.board = dict()

    def _generate_board(self) -> None:
        self.board = {(x, y): tile(x, y, strict=False, filled=False) for x in range(self.board_size) for y in range(self.board_size)}

    def run(self):
        self._clear_board()
        self._generate_board()
        clear_canvas(self.canvas)
        self._update_board()

    def draw(self):
        self._update_board()
