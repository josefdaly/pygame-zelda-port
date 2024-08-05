import pygame
from numpy import zeros, array, random


class Tilemap:
    def __init__(self, tileset, size):
        self.size = size
        self.tileset = tileset
        self.map = zeros(size, dtype=int)
        self.tile_rects = []

        h, w = self.size
        self.image = pygame.Surface((16*w, 16*h))
        self.rect = self.image.get_rect()

    def create_and_render_room(self, collision_tile_map, convert_tile_reference=None):
        m, n = self.map.shape
        tiles = []
        for i in range(m):
            for j in range(n):
                tile_no = self.map[i, j]
                if convert_tile_reference:
                    tile_no = convert_tile_reference(tile_no)
                tile = self.tileset.tiles[tile_no]
                if collision_tile_map[i, j] == 'X':
                    tile_rect = tile.get_rect()
                    tiles.append(tile_rect)
                    tile_rect.y = i*16
                    tile_rect.x = j*16
                    tiles.append(tile_rect)
                self.image.blit(tile, (j*16, i*16))
        self.tile_rects = tiles

    def set_room(self, room, collision_tile_map, convert_tile_reference=None):
        self.map = array(room)
        self.create_and_render_room(collision_tile_map, convert_tile_reference)

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
