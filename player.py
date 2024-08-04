import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, files, horizantal_flip_files, speed=1.8, starting_loc=(0, 0)):
        super().__init__()
        self.images = []
        for file in files:
            self.images.append(pygame.image.load(file).convert_alpha())
        for file in horizantal_flip_files:
            self.images.append(pygame.transform.flip(
                pygame.image.load(file).convert_alpha(),
                True,
                False,
            ))

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.y = starting_loc[0]
        self.rect.x = starting_loc[1]
        self.wall_collision_rect = pygame.Rect(
            starting_loc[1] + 2,
            starting_loc[0] + (self.rect.height/2),
            self.rect.width - 4,
            self.rect.height/2,
        )
        self.speed = speed
        self.velocity = (0, 0)
        self.dir = (0, 0)
        self.is_moving = False
        self.last_time = pygame.time.get_ticks()
        self.time_frame = 200 #ms
        self.walking_frame = 0
        self.DIR_TO_IMAGES_MAP = {
            (0, -1): (self.images[4], self.images[5]),
            (0, 1): (self.images[0], self.images[1]),
            (-1, 0): (self.images[2], self.images[3]),
            (1, 0): (self.images[6], self.images[7]),
        }

    def is_walking_over_edge(self, bottom, right):
        if self.rect.centerx < 0:
            return True
        if self.rect.centery < 0:
            return True
        if self.rect.centerx > right:
            return True
        if self.rect.centery > bottom:
            return True

    def flip_walking_frame(self):
        self.walking_frame = (self.walking_frame + 1) % 2

    def set_walking_image(self):
        self.image = self.DIR_TO_IMAGES_MAP[self.dir][self.walking_frame]

    def set_velocity(self, dir):
        self.is_moving = True
        self.velocity = (self.speed*dir[0], self.speed*dir[1])
        self.dir = dir

    def should_be_moving(self, tile_rects):
        if self.is_moving:
            test_rect = self.wall_collision_rect.move(self.velocity)
            if not test_rect.collidelistall(tile_rects):
                return True
        return False

    def stop(self, dir):
        if dir == self.dir:
            self.is_moving = False
            self.dir = (0, 0)
            self.velocity = (0, 0)

    def time_frame_has_passed(self):
        if self.last_time + self.time_frame < pygame.time.get_ticks():
            self.last_time = pygame.time.get_ticks()
            return True

    def move(self, velocity):
        self.rect.move_ip(velocity)
        self.wall_collision_rect.move_ip(velocity)

    def update_player_location(self):
        if self.is_moving:
            self.move(self.velocity)
            if self.time_frame_has_passed():
                self.flip_walking_frame()
            self.set_walking_image()
