import pygame
from numpy import zeros, array, random


class MapTile:
    """
    Abstraction for instantiated tile on map
    """

    def __init__(self, tile, rect):
        self.tile = tile
        self.rect = rect


class Tilemap:
    def __init__(self, tileset, size, tile_width, tile_height, map_offset):
        self.size = size
        self.tileset = tileset
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map_offset = map_offset
        self.map = zeros(size, dtype=int)
        self.collision_rects = []

        h, w = self.size
        self.image = pygame.Surface((self.tile_width * w, self.tile_height * h))
        self.rect = self.image.get_rect()

    def create_and_render_room(self, collision_tile_map, convert_tile_reference=None):
        m, n = self.map.shape
        self.collision_rects = []
        for i in range(m):
            for j in range(n):
                tile_no = self.map[i, j]
                if convert_tile_reference:
                    tile_no = convert_tile_reference(tile_no)
                tile = self.tileset.tiles[tile_no]
                if collision_tile_map[i, j] == "X":
                    tile_rect = tile.get_rect()
                    tile_rect.y = i * self.tile_height + self.map_offset
                    tile_rect.x = j * self.tile_width
                    self.collision_rects.append(tile_rect)
                self.image.blit(tile, (j * self.tile_width, i * self.tile_height))

    def set_room(self, room, collision_tile_map, convert_tile_reference=None):
        self.map = array(room)
        self.create_and_render_room(collision_tile_map, convert_tile_reference)

    def __str__(self):
        return f"{self.__class__.__name__} {self.size}"
