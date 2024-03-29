import ast
import base64
import math
from dataclasses import dataclass, field

import pygame


NEARBY_TILES = [(0, 1), (0, -1), (1, 0), (-1, 0)]


@dataclass
class tile:

    x: int
    y: int

    color: int = 0x202020
    filled: bool = True
    strict: bool = True

    connected: bool = field(init=False, default=False)
    hit_box: pygame.Rect = field(init=False)


@dataclass
class color:
    red = 0xFF0000
    green = 0x00FF00
    blue = 0x0000FF
    yellow = 0xFFC300
    orange = 0xFF5733
    purple = 0x7D3C98
    pink = 0xFFC0CB
    brown = 0x8B4513
    cyan = 0x00FFFF

    # empty space color
    gray = 0x202020


def clear_canvas(canvas: pygame.Surface):
    canvas.fill(0x202020)


def draw_centered_text(canvas: pygame.Surface, text: pygame.Surface, x: float, y: float) -> None:
    text_rect = text.get_rect()
    canvas.blit(text, (x - text_rect.width/2, y - text_rect.height/2))


def draw_right_align_text(canvas: pygame.Surface, text: pygame.Surface, x: float, y: float) -> None:
    text_rect = text.get_rect()
    canvas.blit(text, (x - text_rect.width, y))


def get_nearby(board: dict[tuple[int, int], tile], x: int, y: int) -> list[tile]:
    return [board[(x + i, y + j)] for i, j in NEARBY_TILES if (x + i, y + j) in board]


def check_filled(board: dict[tuple[int, int], tile]) -> bool:
    return all([board[i].filled for i in board])


def find_color(board: dict[tuple[int, int], tile], c: int) -> list[tile]:
    return [board[i] for i in board if board[i].color == c]


def clear_color(board: dict[tuple[int, int], tile], c: int) -> None:
    for tile_c in find_color(board, c):
        if tile_c.strict:
            tile_c.connected = False
            continue
        tile_c.color = color.gray
        tile_c.filled = False


def check_number_connected(board: dict[tuple[int, int], tile]) -> int:
    return len([board[i] for i in board if board[i].connected]) // 2


def encode_data(board: dict[tuple[int, int], tile], name: str, size: int) -> bytes:
    data = {
        'name': name,
        'size': size,
        'nodes': [((board[i].x, board[i].y), board[i].color) for i in board if board[i].strict and board[i].filled]
    }
    return base64.b64encode(str(data).encode('utf-8'))


def unload_data(data: str) -> dict:
    return ast.literal_eval(base64.b64decode(data).decode())
