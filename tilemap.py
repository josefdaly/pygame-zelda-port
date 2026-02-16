from __future__ import annotations

import pygame
from numpy import zeros, array
import numpy.typing as npt
from typing import Callable

from tileset import Tileset


class MapTile:
    """Abstraction for instantiated tile on map"""

    def __init__(self, tile: pygame.Surface, rect: pygame.Rect) -> None:
        self.tile = tile
        self.rect = rect


class Tilemap:
    def __init__(
        self,
        tileset: Tileset,
        size: tuple[int, int],
        tile_width: int,
        tile_height: int,
        map_offset: int,
    ) -> None:
        self.size = size
        self.tileset = tileset
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map_offset = map_offset
        self.map: npt.NDArray = zeros(size, dtype=int)
        self.collision_rects: list[pygame.Rect] = []

        h, w = self.size
        self.image = pygame.Surface((self.tile_width * w, self.tile_height * h))
        self.rect = self.image.get_rect()

    def create_and_render_room(
        self,
        collision_tile_map: npt.NDArray,
        convert_tile_reference: Callable[[int | str], int] | None = None,
    ) -> None:
        m, n = self.map.shape
        self.collision_rects = []

        if len(self.tileset.tiles) == 0:
            raise ValueError("Tileset has no tiles loaded")

        for i in range(m):
            for j in range(n):
                tile_no = self.map[i, j]
                if convert_tile_reference:
                    tile_no = convert_tile_reference(tile_no)

                if tile_no < 0 or tile_no >= len(self.tileset.tiles):
                    raise ValueError(
                        f"Tile index {tile_no} out of range (max: {len(self.tileset.tiles) - 1})"
                    )

                tile = self.tileset.tiles[tile_no]
                if collision_tile_map[i, j] == "X":
                    tile_rect = tile.get_rect()
                    tile_rect.y = i * self.tile_height + self.map_offset
                    tile_rect.x = j * self.tile_width
                    self.collision_rects.append(tile_rect)
                self.image.blit(tile, (j * self.tile_width, i * self.tile_height))

    def set_room(
        self,
        room: npt.NDArray,
        collision_tile_map: npt.NDArray,
        convert_tile_reference: Callable[[int | str], int] | None = None,
    ) -> None:
        m, n = self.size
        if room.shape != (m, n):
            raise ValueError(
                f"Room shape {room.shape} does not match map size {self.size}"
            )
        self.map = array(room)
        self.create_and_render_room(collision_tile_map, convert_tile_reference)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.size}"
