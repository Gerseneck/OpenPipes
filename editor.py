from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import TYPE_CHECKING

import pygame
from pygame import draw

if TYPE_CHECKING:
    from main import Main

from util import tile, draw_centered_text, clear_canvas, color, find_color


@dataclass
class Editor:
    main: Main
    canvas: pygame.Surface

    board: dict[tuple[int, int], tile] = field(init=False, default_factory=dict)
    board_size: int = field(init=False, default=5)
    board_name: str = field(init=False, default='Untitled Board')
    name_box_selected: bool = field(init=False, default=False)

    color_buttons: dict[int, pygame.rect] = field(init=False, default_factory=dict)
    size_buttons: dict[int, pygame.rect] = field(init=False, default_factory=dict)

    selected_color: int = field(init=False, default=color.gray)

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
    def textbox_rect(self) -> pygame.Rect:
        return pygame.Rect(self.main.x_center - 210 * self.factor, 55, 2 * 210 * self.factor, 2 * 25)

    def _update_board(self) -> None:
        box_size = 350 * self.factor // self.board_size
        x_start = self.main.x_center - (self.board_size * box_size) // 2
        y_start = self.main.y_center - (self.board_size * box_size) // 2 + 15

        draw.rect(self.canvas, 0xffffff, pygame.Rect(x_start - 5, y_start - 5, self.board_size * box_size + 10,
                                                     self.board_size * box_size + 10), 5)

        # level name text box
        text = self.board_name[-28 * self.factor:]
        draw.rect(self.canvas, 0xffffff, self.textbox_rect, 3)
        self.canvas.blit(self.font_24.render(text + '_' if time.time() % 1 > 0.5 and self.name_box_selected else text, True, 0xffffffff),
                         (self.main.x_center - 210 * self.factor + 10, 65))

        # draws color selector
        for i, j in enumerate([i for i in dir(color) if not i.startswith('__')]):
            selected = self.selected_color == getattr(color, j)
            self.color_buttons[getattr(color, j)] = draw.rect(self.canvas, getattr(color, j),
                                                              pygame.Rect(self.main.x_size - 110, 5 + 60 * i, 50, 50), width=(5 if selected else 0))
            if getattr(color, j) == color.gray:
                draw_centered_text(self.canvas, self.font_24.render('\uf12d', True, 0xffffffff), self.main.x_size - 85, 5 + 60 * i + 25)

        # draws board size selector
        for i, j in enumerate(range(5, 10)):
            self.size_buttons[j] = draw.rect(self.canvas, color.blue, pygame.Rect(60, 100 + 50 * i, 50, 50), self.board_size == j)
            draw_centered_text(self.canvas, self.font_24.render(str(j), True, 0xffffff), 85, 100 + 50 * i + 25)

        # draws board
        for i in self.board:
            self.board[i].hit_box = draw.rect(self.canvas, self.board[i].color,
                                              pygame.Rect(x_start + box_size * i[0], y_start + box_size * i[1],
                                                          box_size, box_size), False)
            draw.rect(self.canvas, 0xffffff, pygame.Rect(x_start + box_size * i[0], y_start + box_size * i[1], box_size, box_size), True)

            if self.board[i].strict:
                draw_centered_text(self.canvas, self.font_30.render('X', True, 0x000000),
                                   x_start + box_size // 2 + box_size * i[0], y_start + box_size // 2 + box_size * i[1])

    def _clear_board(self) -> None:
        self.board = dict()

    def _generate_board(self) -> None:
        self.board = {(x, y): tile(x, y, strict=False, filled=False) for x in range(self.board_size) for y in
                      range(self.board_size)}

    def run(self):
        self._clear_board()
        self._generate_board()
        clear_canvas(self.canvas)
        self._update_board()

    def draw(self):
        self._update_board()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.textbox_rect.collidepoint(mouse_pos):
                self.name_box_selected = True
                if self.board_name == 'Untitled Board':
                    self.board_name = ''

            for i in self.color_buttons:
                if self.color_buttons[i].collidepoint(mouse_pos):
                    self.selected_color = i

            for i in self.size_buttons:
                if self.size_buttons[i].collidepoint(mouse_pos):
                    self.board_size = i
                    self.run()

            for i in self.board:
                if self.board[i].hit_box.collidepoint(mouse_pos) and len(find_color(self.board, self.selected_color)) != 2:
                    self.board[i].color = self.selected_color
                    self.board[i].filled = True
                    self.board[i].strict = self.selected_color != color.gray

        if event.type == pygame.KEYDOWN:
            if not self.name_box_selected:
                return

            if event.key == pygame.K_BACKSPACE:
                self.board_name = self.board_name[:-1]

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                if not self.board_name.strip():
                    self.board_name = 'Untitled Board'
                if len(self.board_name) > 37:
                    self.board_name = self.board_name.strip()[:37].strip()
                self.name_box_selected = False

            elif event.key == pygame.K_TAB:
                self.name_box_selected = not self.name_box_selected

            elif self.name_box_selected:
                if event.unicode.isprintable():
                    self.board_name += event.unicode
