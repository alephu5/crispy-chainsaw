#! /usr/bin/python3

import pygame
from pygame.image import load as loadImage
from pygame.locals import KEYDOWN, KEYUP, K_RIGHT, K_LEFT, K_UP, K_DOWN
import os
import string
import itertools

FRAME_RATE = 30

CHAR_PATH = '../assets/Chars/'
ANIMS = ['Hurt', 'Shoot', 'Slash', 'Spellcast', 'Thrust', 'Walk']
INIT_IMG = os.path.join('Walk/Down/tile_130.png')


def sortImages(imageSet):
    "Takes an image set and arranges them in animation order."
    ascii = string.punctuation + string.ascii_letters
    trans = str.maketrans('', '', ascii)
    return sorted(imageSet, key=lambda x: int(x.translate(trans)))


def loadAnims(charName):
    "Gets all animations for the given character."
    animations = {}
    for anim in ANIMS:
        images = {}
        path = os.path.join(CHAR_PATH, charName, anim)
        tree = os.walk(path)
        tree.__next__()
        for dirpath, dirnames, filenames in tree:
            loadedImgs = [loadImage(os.path.join(path, image)) for image in
                          sortImages(filenames)]
            images[os.path.basename(dirpath)] = loadedImgs
        animations[anim] = images
    return animations


class Character(pygame.sprite.Sprite):

    "Allows basic movement and animation."

    def __init__(self, name, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.health = 100
        self.direction = None
        self.speed = 10
        baseimg = os.path.join(CHAR_PATH, name, INIT_IMG)
        anims = loadAnims(name)
        self.image = loadImage(baseimg)
        self.walk = {}
        self.walk[K_RIGHT] = itertools.cycle(anims['Walk']['Right'])
        self.walk[K_LEFT] = itertools.cycle(anims['Walk']['Left'])
        self.walk[K_DOWN] = itertools.cycle(anims['Walk']['Down'])
        self.walk[K_UP] = itertools.cycle(anims['Walk']['Up'])
        self.walk[None] = itertools.cycle([self.image])
        self.images = self.walk[None]

    def changeDirection(self, newDir):
        "Change the image set to animate when the direction changes."
        if newDir != self.direction:
            if newDir in self.walk.keys():
                self.images = self.walk[newDir]
            else:
                self.images = self.walk[None]
            self.direction = None

    def update(self, deltaT):
        x, y = self.position
        if self.direction == K_RIGHT:
            x += self.speed
        if self.direction == K_LEFT:
            x -= self.speed
        if self.direction == K_UP:
            y -= self.speed
        if self.direction == K_DOWN:
            y += self.speed
        image = self.images.__next__()
        self.image = image
        self.position = (x, y)
        # self.rect = self.image.get_rect()
        self.rect.center = self.position


def main():
    screen = pygame.display.set_mode((1024, 768))
    rect = screen.get_rect()
    dave = Character('Dave', rect.center)
    char_group = pygame.sprite.RenderPlain(dave)
    clock = pygame.time.Clock()
    while True:
        deltaT = clock.tick(FRAME_RATE)
        for event in pygame.event.get():
            pygame.event.get()
            if hasattr(event, 'key'):
                if event.type == KEYDOWN:
                    dave.changeDirection(event.key)
                elif event.type == KEYUP:
                    dave.changeDirection(None)
        screen.fill((0, 0, 0))
        char_group.update(deltaT)
        char_group.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()
