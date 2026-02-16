from __future__ import annotations
import os
from typing import Iterator

import pygame


class Tile(pygame.Surface):
    def __init__(self, size: tuple[int, int], number: int) -> None:
        super().__init__(size)
        self.number = number


class Tileset:
    def __init__(
        self,
        file: str,
        size: tuple[int, int],
        margin: int = 1,
        spacing: int = 1,
    ) -> None:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Tileset file not found: {file}")

        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles: list[Tile] = []
        self.load()

    def load(self) -> None:
        self.tiles = []
        x0 = y0 = self.margin
        wi, he = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        count = 0
        for y in range(y0, he, dy):
            for x in range(x0, wi, dx):
                tile = Tile(self.size, count)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)
                count += 1

    def __str__(self) -> str:
        return f"{self.__class__.__name__} file:{self.file} tile:{self.size}"
