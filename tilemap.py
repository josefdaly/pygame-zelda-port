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
    def __init__(self, game, tileset, size):
        self.game = game
        self.size = size
        self.tileset = tileset
        self.map = zeros(size, dtype=int)
        self.collision_rects = []

        h, w = self.size
        self.image = pygame.Surface((self.game.TILE_WIDTH*w, self.game.TILE_HEIGHT*h))
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
                if collision_tile_map[i, j] == 'X':
                    tile_rect = tile.get_rect()
                    tile_rect.y = i*self.game.TILE_HEIGHT + self.game.MAIN_TILE_MAP_LOC[1]
                    tile_rect.x = j*self.game.TILE_WIDTH
                    self.collision_rects.append(tile_rect)
                self.image.blit(tile, (j*self.game.TILE_WIDTH, i*self.game.TILE_HEIGHT))

    def set_room(self, room, collision_tile_map, convert_tile_reference=None):
        self.map = array(room)
        self.create_and_render_room(collision_tile_map, convert_tile_reference)

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
