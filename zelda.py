from __future__ import annotations

import os

import pygame
import pygame.sprite

from tileset import Tileset
from tilemap import Tilemap
from player import Player
from utils import (
    find_map_tile_location,
    parse_overworld_data,
    blockshaped,
    hex_reference_to_integer_from_int,
)


overworld_tile_file = "assets/overworldtiles.png"
player_files: tuple[str, ...] = (
    "assets/link_down1.png",
    "assets/link_down2.png",
    "assets/link_left1.png",
    "assets/link_left2.png",
    "assets/link_up1.png",
    "assets/link_up2.png",
)
horizantal_flip_files: tuple[str, ...] = (
    "assets/link_left1.png",
    "assets/link_left2.png",
)
overworld_music_file = "assets/overworld.mp3"
ROOM_WIDTH = 16
ROOM_HEIGHT = 11
OVERWORLD_COLS = 16
STARTING_TILE = 117
FPS = 60


class Game:
    SCREEN_WIDTH = 256
    SCREEN_HEIGHT = 240

    INFO_VIEW_LOC = (0, -176)
    MAIN_TILE_MAP_OFFSET = 65
    MAIN_TILE_MAP_LOC = (0, MAIN_TILE_MAP_OFFSET)

    W = 256
    H = 176

    INFO_WIDTH = 256
    INFO_HEIGHT = 240

    SIZE = W, H

    TILE_WIDTH = 16
    TILE_HEIGHT = 16

    ROOM_HEIGHT_PIXELS = ROOM_HEIGHT * TILE_HEIGHT
    ROOM_WIDTH_PIXELS = ROOM_WIDTH * TILE_WIDTH
    PLAYER_MOVEMENT_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

    DIR_UP: tuple[int, int] = (0, -1)
    DIR_DOWN: tuple[int, int] = (0, 1)
    DIR_LEFT: tuple[int, int] = (-1, 0)
    DIR_RIGHT: tuple[int, int] = (1, 0)

    DIR_MAP: dict[int, tuple[int, int]] = {
        pygame.K_UP: DIR_UP,
        pygame.K_DOWN: DIR_DOWN,
        pygame.K_LEFT: DIR_LEFT,
        pygame.K_RIGHT: DIR_RIGHT,
    }

    def __init__(self) -> None:
        if not os.path.exists(overworld_tile_file):
            raise FileNotFoundError(f"Tileset not found: {overworld_tile_file}")

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SCALED
        )
        self.info_screen = pygame.Surface((self.INFO_WIDTH, self.INFO_HEIGHT))
        self.info_screen.fill((0, 0, 0))

        pygame.display.set_caption("Zelda")
        self.tileset = Tileset(
            overworld_tile_file, size=(self.TILE_HEIGHT, self.TILE_WIDTH)
        )
        self.tilemap = Tilemap(
            self.tileset,
            size=(ROOM_HEIGHT, ROOM_WIDTH),
            tile_width=self.TILE_WIDTH,
            tile_height=self.TILE_HEIGHT,
            map_offset=self.MAIN_TILE_MAP_OFFSET,
        )
        self.next_tilemap: Tilemap | None = None
        self.next_tilemap_loc: tuple[int, int] | None = None
        self.player = Player(
            player_files,
            horizantal_flip_files,
            starting_loc=find_map_tile_location(
                STARTING_TILE, ROOM_WIDTH, self.TILE_HEIGHT, self.TILE_WIDTH
            ),
        )
        self.sprite_list = pygame.sprite.Group()
        self.sprite_list.add(self.player)
        self.clock = pygame.time.Clock()
        self.running = True
        self.changing_rooms = False
        self.tilemap_velocity: tuple[int, int] = (0, 0)
        self.tilemap_loc: tuple[int, int] = self.MAIN_TILE_MAP_LOC
        self.current_room: tuple[int, int] = (7, 7)
        self.overworld_rooms = blockshaped(
            parse_overworld_data("assets/nes_zelda_overworld_tile_map.txt", " "),
            ROOM_HEIGHT,
            ROOM_WIDTH,
        )
        self.overworld_rooms_collision_data = blockshaped(
            parse_overworld_data("assets/nes_zelda_overworld_blocking_map.txt"),
            ROOM_HEIGHT,
            ROOM_WIDTH,
        )

        if os.path.exists(overworld_music_file):
            pygame.mixer.music.load(overworld_music_file)

    def move_tilemap(self) -> None:
        if self.changing_rooms:
            self.tilemap_loc = (
                self.tilemap_loc[0] + self.tilemap_velocity[0],
                self.tilemap_loc[1] + self.tilemap_velocity[1],
            )
            if self.next_tilemap_loc:
                self.next_tilemap_loc = (
                    self.next_tilemap_loc[0] + self.tilemap_velocity[0],
                    self.next_tilemap_loc[1] + self.tilemap_velocity[1],
                )
            self.player.move(self.tilemap_velocity)

    def handle_player_movement(self) -> None:
        if not self.changing_rooms and self.player.should_be_moving(
            self.tilemap.collision_rects
        ):
            self.player.update()

    def handle_room_change_state(self) -> None:
        if self.player.is_walking_over_edge(
            self.ROOM_HEIGHT_PIXELS + self.MAIN_TILE_MAP_OFFSET,
            self.ROOM_WIDTH_PIXELS,
            self.MAIN_TILE_MAP_LOC[1],
            0,
        ):
            if not self.changing_rooms:
                self.tilemap_velocity = (
                    self.player.dir[0] * -1,
                    self.player.dir[1] * -1,
                )
                self.next_tilemap = Tilemap(
                    self.tileset,
                    size=(ROOM_HEIGHT, ROOM_WIDTH),
                    tile_width=self.TILE_WIDTH,
                    tile_height=self.TILE_HEIGHT,
                    map_offset=self.MAIN_TILE_MAP_OFFSET,
                )

                new_room_row = self.current_room[0] + self.player.dir[1]
                new_room_col = self.current_room[1] + self.player.dir[0]

                if (
                    new_room_row < 0
                    or new_room_row >= len(self.overworld_rooms) // OVERWORLD_COLS
                ):
                    self.changing_rooms = False
                    self.next_tilemap = None
                    return

                self.current_room = (new_room_row, new_room_col)

                room_index = (
                    self.current_room[0] * OVERWORLD_COLS + self.current_room[1]
                )
                self.next_tilemap.set_room(
                    self.overworld_rooms[room_index],
                    self.overworld_rooms_collision_data[room_index],
                    convert_tile_reference=hex_reference_to_integer_from_int,
                )
                self.next_tilemap_loc = (
                    self.ROOM_WIDTH_PIXELS * self.player.dir[0],
                    self.ROOM_HEIGHT_PIXELS * self.player.dir[1]
                    + self.MAIN_TILE_MAP_OFFSET,
                )
            self.changing_rooms = True

        if self.next_tilemap and self.changing_rooms:
            if self.next_tilemap_loc == self.MAIN_TILE_MAP_LOC:
                self.player.move(self.player.velocity)
                self.changing_rooms = False
                self.tilemap = self.next_tilemap
                self.tilemap_loc = self.MAIN_TILE_MAP_LOC
                self.next_tilemap = None
                self.next_tilemap_loc = None
                self.tilemap_velocity = (0, 0)

    def render_info_screen(self) -> None:
        self.screen.blit(self.info_screen, self.INFO_VIEW_LOC)

    def render_tilemap(self) -> None:
        self.screen.blit(self.tilemap.image, self.tilemap_loc)

    def render_next_tilemap(self) -> None:
        if self.next_tilemap and self.next_tilemap_loc:
            self.screen.blit(self.next_tilemap.image, self.next_tilemap_loc)

    def run(self) -> None:
        room_index = self.current_room[0] * OVERWORLD_COLS + self.current_room[1]
        self.tilemap.set_room(
            self.overworld_rooms[room_index],
            self.overworld_rooms_collision_data[room_index],
            convert_tile_reference=hex_reference_to_integer_from_int,
        )
        self.render_tilemap()
        self.render_info_screen()

        if os.path.exists(overworld_music_file):
            pygame.mixer.music.play(-1)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.PLAYER_MOVEMENT_KEYS:
                        self.player.set_velocity(self.DIR_MAP[event.key])
                elif event.type == pygame.KEYUP:
                    if event.key in self.PLAYER_MOVEMENT_KEYS:
                        self.player.stop(self.DIR_MAP[event.key])

            self.handle_player_movement()
            self.handle_room_change_state()
            self.move_tilemap()
            self.update_display()
            self.clock.tick(FPS)
        pygame.quit()

    def update_display(self) -> None:
        self.render_tilemap()
        if self.next_tilemap:
            self.render_next_tilemap()
            self.render_info_screen()
        self.sprite_list.draw(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
