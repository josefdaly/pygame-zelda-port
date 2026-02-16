from __future__ import annotations

import os

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        files: tuple[str, ...],
        horizantal_flip_files: tuple[str, ...],
        speed: float = 1.8,
        starting_loc: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__()
        self.images: list[pygame.Surface] = []
        loaded_images: dict[str, pygame.Surface] = {}

        for file in files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Player sprite file not found: {file}")
            if file not in loaded_images:
                loaded_images[file] = pygame.image.load(file).convert_alpha()
            self.images.append(loaded_images[file])

        for file in horizantal_flip_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Player sprite file not found: {file}")
            if file not in loaded_images:
                loaded_images[file] = pygame.image.load(file).convert_alpha()
            self.images.append(pygame.transform.flip(loaded_images[file], True, False))

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.y = starting_loc[0]
        self.rect.x = starting_loc[1]
        self.wall_collision_rect = pygame.Rect(
            starting_loc[1] + 2,
            starting_loc[0] + (self.rect.height // 2),
            self.rect.width - 4,
            self.rect.height // 2,
        )
        self.speed = speed
        self.velocity: tuple[float, float] = (0.0, 0.0)
        self.dir: tuple[int, int] = (0, 1)
        self.is_moving = False
        self.last_time = pygame.time.get_ticks()
        self.time_frame = 200  # ms
        self.walking_frame = 0
        self.DIR_TO_IMAGES_MAP: dict[
            tuple[int, int], tuple[pygame.Surface, pygame.Surface]
        ] = {
            (0, -1): (self.images[4], self.images[5]),
            (0, 1): (self.images[0], self.images[1]),
            (-1, 0): (self.images[2], self.images[3]),
            (1, 0): (self.images[6], self.images[7]),
        }

    def is_walking_over_edge(
        self,
        bottom: int,
        right: int,
        top: int,
        left: int,
    ) -> bool:
        if self.rect.centerx < left:
            return True
        if self.rect.centery < top:
            return True
        if self.rect.centerx > right:
            return True
        if self.rect.centery > bottom:
            return True
        return False

    def flip_walking_frame(self) -> None:
        self.walking_frame = (self.walking_frame + 1) % 2

    def set_walking_image(self) -> None:
        self.image = self.DIR_TO_IMAGES_MAP[self.dir][self.walking_frame]

    def set_velocity(self, dir: tuple[int, int]) -> None:
        self.is_moving = True
        self.velocity = (self.speed * dir[0], self.speed * dir[1])
        self.dir = dir

    def should_be_moving(self, tile_rects: list[pygame.Rect]) -> bool:
        if self.is_moving:
            test_rect = self.wall_collision_rect.move(self.velocity)
            if not test_rect.collidelistall(tile_rects):
                return True
        return False

    def stop(self, dir: tuple[int, int]) -> None:
        if dir == self.dir:
            self.is_moving = False
            self.dir = (0, 0)
            self.velocity = (0.0, 0.0)

    def time_frame_has_passed(self) -> bool:
        if self.last_time + self.time_frame < pygame.time.get_ticks():
            self.last_time = pygame.time.get_ticks()
            return True
        return False

    def move(self, velocity: tuple[float, float]) -> None:
        self.rect.move_ip(velocity)
        self.wall_collision_rect.move_ip(velocity)

    def update(self) -> None:
        if self.is_moving:
            self.move(self.velocity)
            if self.time_frame_has_passed():
                self.flip_walking_frame()
            self.set_walking_image()
