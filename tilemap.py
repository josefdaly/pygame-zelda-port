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

    def create_and_render_room(self, collision_tile_map):
        m, n = self.map.shape
        tiles = []
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                if collision_tile_map.get(tile.number):
                    tile_rect = tile.get_rect()
                    tiles.append(tile_rect)
                    tile_rect.y = i*16
                    tile_rect.x = j*16
                    tiles.append(tile_rect)
                self.image.blit(tile, (j*16, i*16))
        self.tile_rects = tiles

    def set_room(self, room, collision_tile_map):
        self.map = array(room)
        print(self.map)
        print(self.map.shape)
        self.create_and_render_room(collision_tile_map)

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
