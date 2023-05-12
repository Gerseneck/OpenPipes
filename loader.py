from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import TYPE_CHECKING

import pygame
from pygame import draw

if TYPE_CHECKING:
    from main import Main

from util import clear_canvas


@dataclass
class Loader:
    main: Main
    canvas: pygame.Surface

    text: str = field(init=False, default='Enter the data here.')

    invalid_data: bool = field(init=False, default=False)

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
        text = self.text[-28 * self.factor:]
        draw.rect(self.canvas, 0xffffff, self.textbox_rect, 3)
        self.canvas.blit(self.font_24.render(text + '_' if time.time() % 1 > 0.5 else text, True, 0xffffffff),
                         (self.main.x_center - 210 * self.factor + 10, 65))

    def run(self):
        clear_canvas(self.canvas)
        self._update_board()

    def draw(self):
        self._update_board()

    def handle_event(self, event: pygame.event.Event):

        if event.type == pygame.KEYDOWN:
            if self.text == 'Enter the data here.':
                self.text = ''

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                self.text += pygame.scrap.get('text/plain;charset=utf-8').decode('utf-8')

            else:
                if event.unicode.isprintable():
                    self.text += event.unicode
