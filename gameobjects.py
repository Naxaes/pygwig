import pygame
import numpy as np
import math


class Projectile(pygame.sprite.Sprite):

    def __init__(self, image, position, direction, speed):
        super(Projectile, self).__init__()
        self.image = image
        self.rect = image.get_rect(topleft=position)

        self.position = np.array(position, np.float16)
        self.velocity = np.array(direction, np.float16) / math.sqrt(direction[0] ** 2 + direction[1] ** 2) * speed

    def update(self):
        self.position += self.velocity
        self.rect.topleft = self.position
