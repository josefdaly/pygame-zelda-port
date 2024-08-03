import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, files, speed=1, starting_loc=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for file in files:
            self.images.append(pygame.image.load(file).convert_alpha())
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.y = starting_loc[0]
        self.rect.x = starting_loc[1]
        self.speed = speed
        self.velocity = (0, 0)
        self.dir = (0, 0)

    def set_velocity(self, dir):
        self.velocity = (self.speed*dir[0], self.speed*dir[1])
        self.dir = dir

    def stop(self, dir):
        if dir == self.dir:
            self.dir = (0, 0)
            self.velocity = (0, 0)

    def update_player_location(self):
        self.rect.move_ip(self.velocity)
