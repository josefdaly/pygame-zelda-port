import pygame
from numpy import zeros, array, random


class Tilemap:
    def __init__(self, tileset, size):
        self.size = size
        self.tileset = tileset
        self.map = zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((16*w, 16*h))
        self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*16, i*16))

    def set_room(self, room):
        self.map = array(room)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_zero(self):
        self.map = zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
