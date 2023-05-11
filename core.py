from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pygame
from pygame import draw

from data.level import LEVELS
from util import tile, clear_canvas, draw_centered_text, clear_color, get_nearby, check_filled, color, encode_data

if TYPE_CHECKING:
    from main import Main


@dataclass
class Core:
    main: Main
    canvas: pygame.Surface

    board: dict[tuple[int, int], tile] = field(init=False, default_factory=dict)
    loaded: bool = field(init=False, default=False)

    level: int = field(init=False, default=0)
    level_name: str = field(init=False)
    level_size: int = field(init=False)
    level_nodes: list[tuple[tuple[int, int], int]] = field(init=False)
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

    def _update_board(self) -> None:
        box_size = 350 * self.factor // self.level_size
        x_start = self.main.x_center - (self.level_size * box_size) // 2
        y_start = self.main.y_center - (self.level_size * box_size) // 2 + 15

        draw.rect(self.canvas, 0xffffff, pygame.Rect(x_start - 5, y_start - 5, self.level_size * box_size + 10,
                                                     self.level_size * box_size + 10), 5)

        for i in self.board:
            self.board[i].hit_box = draw.rect(self.canvas, self.board[i].color,
                                              pygame.Rect(x_start + box_size * i[0], y_start + box_size * i[1],
                                                          box_size, box_size), False)
            if self.board[i].strict:
                draw_centered_text(self.canvas,
                                   self.font_30.render('\u2713' if self.board[i].connected else 'X', True, 0x000000),
                                   x_start + box_size // 2 + box_size * i[0], y_start + box_size // 2 + box_size * i[1])

    def _create_board(self) -> None:
        if self.level_nodes:
            for i in self.level_nodes:
                self.board[i[0]] = tile(*i[0], color=i[1])
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

        self.level = level
        self.level_name = LEVELS[level]['name']
        self.level_size = LEVELS[level]['size']
        self.level_nodes = LEVELS[level]['nodes']
        self.required = len(LEVELS[level]['nodes']) // 2
        self.time_start = self.main.number_tick

        self._create_board()
        clear_canvas(self.canvas)
        self._update_board()

    def run_game_special(self, data: dict) -> None:
        self._clear_board()

        self.level = -1
        self.level_name = data['name']
        self.level_size = data['size']
        self.level_nodes = data['nodes']
        self.required = len(data['nodes']) // 2
        self.time_start = self.main.number_tick
        self.loaded = True

        self._create_board()
        clear_canvas(self.canvas)
        self._update_board()

    def draw(self):
        self._update_board()
        
    def handle_event(self, event: pygame.event) -> bool:
        """Handle events for the game, returns True if the game is over"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for i, j in self.board:
                t1 = self.board[(i, j)]
                if t1.hit_box.collidepoint(mouse_pos) and t1.strict and t1.color != color.gray:
                    if t1.connected:
                        clear_color(self.board, t1.color)
                        self.selected = None
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
                            self.time_end = self.main.number_tick
                            return True
                        continue
                    if t1.strict:
                        continue
                    if is_color_nearby:
                        if t1.filled and t1.color != select_color:
                            clear_color(self.board, t1.color)
                        t1.color = select_color
                        t1.filled = True
        return False
                        