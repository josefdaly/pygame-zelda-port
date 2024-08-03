import pygame

from tileset import Tileset
from tilemap import Tilemap
from player import Player
from utils import find_map_tile_location
from levels.overworld import STARTING_ROOM

overworld_tile_file = 'assets/overworldtiles.png'
player_files = (
    'assets/link_down1.png',
    'assets/link_down2.png',
    'assets/link_left1.png',
    'assets/link_left2.png',
    'assets/link_up1.png',
    'assets/link_up2.png',
)
horizantal_flip_files = (
    'assets/link_left1.png',
    'assets/link_left2.png',
)
TILE_WIDTH = 16
TILE_HEIGHT = 16
ROOM_WIDTH = 16
ROOM_HEIGHT = 11
FPS = 60

class Game:
    W = 256
    H = 240
    SIZE = W, H

    PLAYER_MOVEMENT_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
    DIR_MAP = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE, pygame.SCALED)
        pygame.display.set_caption("Zelda")
        self.tileset = Tileset(overworld_tile_file, size=(TILE_HEIGHT, TILE_WIDTH))
        self.tilemap = Tilemap(self.tileset, size=(ROOM_HEIGHT, ROOM_WIDTH))
        self.player = Player(
            player_files,
            horizantal_flip_files,
            starting_loc=find_map_tile_location(117, ROOM_WIDTH, TILE_HEIGHT, TILE_WIDTH)
        )
        self.sprite_list = pygame.sprite.Group()
        self.sprite_list.add(self.player)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        self.tilemap.set_room(STARTING_ROOM)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.PLAYER_MOVEMENT_KEYS:
                        dir = self.DIR_MAP[event.key]
                        self.player.set_velocity(dir)
                elif event.type == pygame.KEYUP:
                    if event.key in self.PLAYER_MOVEMENT_KEYS:
                        dir = self.DIR_MAP[event.key]
                        self.player.stop(dir)
                        print(self.player.dir, self.player.velocity)
            self.player.update_player_location()
            self.update_display()
            self.clock.tick(FPS)
        pygame.quit()

    def update_display(self):
        self.screen.blit(self.tilemap.image, (0,0))
        self.sprite_list.draw(self.screen)
        pygame.display.update()


game = Game()
game.run()
