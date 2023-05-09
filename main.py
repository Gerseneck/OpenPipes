from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

import pygame


__version__ = '0.0.1'

from game import Game


@dataclass
class Main:
    TPS: ClassVar[int] = 60
    x_size: int = 800
    y_size: int = 600

    number_tick: int = field(init=False, default=0)

    @property
    def x_center(self) -> int:
        return self.x_size // 2

    @property
    def y_center(self) -> int:
        return self.y_size // 2

    def main(self) -> None:
        pygame.init()
        # logo = pygame.image.load('assets/logo.png')
        # pygame.display.set_icon(logo)
        pygame.display.set_caption(f'OpenPipe {__version__}')
        canvas = pygame.display.set_mode((self.x_size, self.y_size))
        clock = pygame.time.Clock()

        game = Game(self, canvas)
        game.main_menu()

        while True:
            self.number_tick += 1
            clock.tick(self.TPS)
            game.tick_loop()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.VIDEORESIZE:
                    self.x_size = event.w
                    self.y_size = event.h
                game.handle_event(event)


if __name__ == '__main__':
    Main().main()
