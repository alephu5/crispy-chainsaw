#! /usr/bin/python3

import pygame
# from pygame.locals import FULLSCREEN, DOUBLEBUF

FRAME_RATE = 30


class Character(pygame.sprite.Sprite):
    INIT_HEALTH = 100

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.health = INIT_HEALTH
        self.up = self.right = 0

    def update(self, deltaT):
        pass


def main():
    screen = pygame.display.set_mode((1024, 768))
