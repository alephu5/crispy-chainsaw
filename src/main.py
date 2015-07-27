#! /usr/bin/python3

import pygame
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN

FRAME_RATE = 30


class Character(pygame.sprite.Sprite):

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.health = 100
        self.moveup = self.moveright = 0

    def update(self, deltaT):
        x, y = self.position
        x += self.moveright
        y += self.moveup
        self.moveright = self.moveleft = 0
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


def main():
    screen = pygame.display.set_mode((1024, 768))
    rect = screen.get_rect()
    dave = Character('walker.png', rect.center)
    char_group = pygame.sprite.RenderPlain(dave)
    clock = pygame.time.Clock()
    while True:
        deltaT = clock.tick(FRAME_RATE)
        for event in pygame.event.get():
            pygame.event.get()
            if hasattr(event, 'key'):
                pressed = (event.type == KEYDOWN)
                if event.key == K_RIGHT:
                    dave.moveright += pressed * 1
                if event.key == K_LEFT:
                    dave.moveright += pressed * (-1)
                if event.key == K_UP:
                    dave.moveup += pressed * 1
                if event.key == K_DOWN:
                    dave.moveup += pressed * (-1)
        screen.fill((0, 0, 0))
        char_group.update(deltaT)
        char_group.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()
