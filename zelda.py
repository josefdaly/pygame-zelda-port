import pygame

from tileset import Tileset
from tilemap import Tilemap
from player import Player
from utils import find_map_tile_location, parse_overworld_data, blockshaped, hex_reference_to_integer
from levels.overworld import STARTING_ROOM, COLLISION_TILES, ROOM_MATRIX

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
    H = 176
    SIZE = W, H
    ROOM_HEIGHT_PIXELS = ROOM_HEIGHT * TILE_HEIGHT
    ROOM_WIDTH_PIXELS = ROOM_WIDTH * TILE_WIDTH
    PLAYER_MOVEMENT_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    DIR_UP = (0, -1)
    DIR_DOWN = (0, 1)
    DIR_LEFT = (-1, 0)
    DIR_RIGHT = (1, 0)

    DIR_MAP = {
        pygame.K_UP: DIR_UP,
        pygame.K_DOWN: DIR_DOWN,
        pygame.K_LEFT: DIR_LEFT,
        pygame.K_RIGHT: DIR_RIGHT,
    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE, pygame.SCALED)
        pygame.display.set_caption("Zelda")
        self.tileset = Tileset(overworld_tile_file, size=(TILE_HEIGHT, TILE_WIDTH))
        self.tilemap = Tilemap(self.tileset, size=(ROOM_HEIGHT, ROOM_WIDTH))
        self.next_tilemap = None
        self.next_tilemap_loc = None
        self.player = Player(
            player_files,
            horizantal_flip_files,
            starting_loc=find_map_tile_location(117, ROOM_WIDTH, TILE_HEIGHT, TILE_WIDTH)
        )
        self.sprite_list = pygame.sprite.Group()
        self.sprite_list.add(self.player)
        self.clock = pygame.time.Clock()
        self.running = True
        self.changing_rooms = False
        self.tilemap_velocity = (0, 0)
        self.tilemap_loc = (0 ,0)
        self.current_room = (7, 7)
        self.overworld_rooms = blockshaped(
            parse_overworld_data('assets/nes_zelda_overworld_tile_map.txt', ' '),
            ROOM_HEIGHT,
            ROOM_WIDTH,
        )
        self.overworld_rooms_collision_data = blockshaped(
            parse_overworld_data('assets/nes_zelda_overworld_blocking_map.txt'),
            ROOM_HEIGHT,
            ROOM_WIDTH,
        )

    def move_tilemap(self):
        if self.changing_rooms:
            self.tilemap_loc = (
                self.tilemap_loc[0] + self.tilemap_velocity[0],
                self.tilemap_loc[1] + self.tilemap_velocity[1],
            )
            self.next_tilemap_loc = (
                self.next_tilemap_loc[0] + self.tilemap_velocity[0],
                self.next_tilemap_loc[1] + self.tilemap_velocity[1],
            )
            self.player.move(self.tilemap_velocity)

    def run(self):
        self.tilemap.set_room(
            self.overworld_rooms[self.current_room[0] * 16 + self.current_room[1]],
            self.overworld_rooms_collision_data[self.current_room[0] * 16 + self.current_room[1]],
            convert_tile_reference=hex_reference_to_integer,
        )
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.PLAYER_MOVEMENT_KEYS:
                        dir = self.DIR_MAP[event.key]
                        self.player.set_velocity(dir)
                    if event.key == pygame.K_a:
                        self.changing_rooms = True
                        self.tilemap_velocity = (-1, 0)
                elif event.type == pygame.KEYUP:
                    if event.key in self.PLAYER_MOVEMENT_KEYS:
                        dir = self.DIR_MAP[event.key]
                        self.player.stop(dir)

            if not self.changing_rooms and self.player.should_be_moving(self.tilemap.tile_rects):
                self.player.update_player_location()

            if self.player.is_walking_over_edge(self.ROOM_HEIGHT_PIXELS, self.ROOM_WIDTH_PIXELS):
                if not self.changing_rooms:
                    self.tilemap_velocity = (self.player.dir[0] * -1, self.player.dir[1] * -1)
                    self.next_tilemap = Tilemap(self.tileset, size=(ROOM_HEIGHT, ROOM_WIDTH))
                    self.current_room = (
                        self.current_room[0] + self.player.dir[1],
                        self.current_room[1] + self.player.dir[0],
                    )
                    self.next_tilemap.set_room(
                        self.overworld_rooms[self.current_room[0] * 16 + self.current_room[1]],
                        self.overworld_rooms_collision_data[self.current_room[0] * 16 + self.current_room[1]],
                        convert_tile_reference=hex_reference_to_integer,
                    )
                    self.next_tilemap_loc = (self.ROOM_WIDTH_PIXELS * self.player.dir[0], self.ROOM_HEIGHT_PIXELS * self.player.dir[1])
                self.changing_rooms = True

            if self.next_tilemap and self.changing_rooms == True:
                if self.next_tilemap_loc == (0, 0):
                    self.player.move(self.player.velocity)
                    self.changing_rooms = False
                    self.tilemap = self.next_tilemap
                    self.tilemap_loc = (0, 0)
                    self.next_tilemap = None
                    self.next_tilemap_loc = None
                    self.tilemap_velocity = (0, 0)

            self.move_tilemap()
            self.update_display()
            self.clock.tick(FPS)
        pygame.quit()

    def update_display(self):
        self.screen.blit(self.tilemap.image, self.tilemap_loc)
        if self.next_tilemap:
            self.screen.blit(self.next_tilemap.image, self.next_tilemap_loc)
        self.sprite_list.draw(self.screen)
        pygame.display.update()


game = Game()
game.run()
