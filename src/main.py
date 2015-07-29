#! /usr/bin/python3

import pygame
from pygame.image import load as loadImage
from pygame.locals import (K_LEFT, K_RIGHT, K_UP, K_DOWN,
                           K_ESCAPE, QUIT, KEYDOWN, KEYUP)
import pygame.mixer
from pygame.mixer import music
from pytmx.util_pygame import load_pygame
import pyscroll
import os
import string
import itertools

FRAME_RATE = 90
IMAGE_RATE = 30
CHAR_PATH = '../assets/Chars/'
ANIMS = ['Hurt', 'Shoot', 'Slash', 'Spellcast', 'Thrust', 'Walk', 'WalkCollsion']
MUSIC = '../assets/Music/Soliloquy_1.ogg'
INIT_IMG = os.path.join('Walk/Down/tile_130.png')
SCREEN_SIZE = 1024, 768
MAP_PATH = '../assets/base.tmx'


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
            direction = os.path.basename(dirpath)
            loadedImgs = [loadImage(os.path.join(path, direction, image))
                          for image in sortImages(filenames)]
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
        self.speed = 150/1000
        self.obstructed = False
        baseimg = os.path.join(CHAR_PATH, name, INIT_IMG)
        anims = loadAnims(name)
        self.image = loadImage(baseimg)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # Load images for animation.
        self.walk = {}
        self.walk[K_RIGHT] = itertools.cycle(anims['Walk']['Right'])
        self.walk[K_LEFT] = itertools.cycle(anims['Walk']['Left'])
        self.walk[K_DOWN] = itertools.cycle(anims['Walk']['Down'])
        self.walk[K_UP] = itertools.cycle(anims['Walk']['Up'])
        self.walk[None] = itertools.cycle([self.image])
        self.images = self.walk[None]
        self.imageclock = 0  # Tracks how long an image is on the screen.
        self.imagerate = IMAGE_RATE  # Images per second.

    def changeDirection(self, newDir):
        "Change the image set to animate when the direction changes."
        if newDir != self.direction:
            if newDir in self.walk.keys():
                self.images = self.walk[newDir]
                self.image = self.images.__next__()
                self.mask = pygame.mask.from_surface(self.image)
                self.direction = newDir
                self.obstructed = False
                self.imageclock = 0
            else:
                self.images = self.walk[None]
                self.direction = None

    def update(self, deltaT):
        x, y = self.position
        if not self.obstructed:
            if self.direction == K_RIGHT:
                x += self.speed * deltaT
            if self.direction == K_LEFT:
                x -= self.speed * deltaT
            if self.direction == K_UP:
                y -= self.speed * deltaT
            if self.direction == K_DOWN:
                y += self.speed * deltaT
        self.imageclock += deltaT
        if self.imageclock >= 1000 / self.imagerate:
            self.image = self.images.__next__()
            self.imageclock = 0
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class Game:

    def __init__(self, screen_size, map, bgmusic=None):
        pygame.init()
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.map = load_pygame(map)
        self.running = False
        self.group = pyscroll.PyscrollGroup()
        self.obstacles = pygame.sprite.Group()
        # Use pyscroll to ensure that the camera tracks the player and does
        # not go off the edge.
        map_data = pyscroll.TiledMapData(self.map)
        map_layer = pyscroll.BufferedRenderer(
            map_data,
            screen_size,
            clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer,
            default_layer=1)
        if bgmusic:
            self.music = music.load(bgmusic)
        else:
            self.music = None

    def load_obstacles(self):
        """Assumes that all tiles in the foreground block motion. Draws
        rectangles around each tile and creates a collision map."""
        for tile in self.map.layers[1].tiles():
            x, y, img = tile
            obstacle = pygame.sprite.Sprite()
            obstacle.rect = img.get_rect()
            # Multiply by 32 because the tiles are 32x32 across.
            obstacle.rect.center = (x*32, y*32)
            obstacle.mask = pygame.mask.from_surface(img)
            self.obstacles.add(obstacle)

    def addPlayer(self, character):
        self.player = character
        self.group.add(character)
        self.group.center(character.position)

    def update(self, deltaT):
        # Check for collision and block motion if true. When the direction
        # changes, allow the player to take one step before checking
        # for collision.
        if pygame.sprite.spritecollideany(self.player, self.obstacles,
                                          collided=pygame.sprite.collide_mask):
            self.player.obstructed = True

        # Check for input and simulate motion.
        for event in pygame.event.get():
            pygame.event.get()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Kill the game if the escape key is pressed.
                    self.running = False
                else:
                    # Move in the given direction when key is presed.
                    self.player.changeDirection(event.key)
            elif event.type == KEYUP:
                # Stop moving when the key is released.
                self.player.changeDirection(None)
            elif event.type == QUIT:
                self.running = False
        # Test for collisions.

        self.group.center(self.player.position)
        self.group.update(deltaT)
        self.group.draw(self.screen)
        pygame.display.update()

    def start(self, frame_rate):
        self.group.draw(self.screen)
        music.play(-1)
        self.running = True
        while self.running:
            deltaT = self.clock.tick(frame_rate)
            self.update(deltaT)
        if self.music:
            music.stop(self.music)


def main():
    new_game = Game(SCREEN_SIZE, MAP_PATH, MUSIC)
    dave = Character('Dave', new_game.rect.center)
    new_game.load_obstacles()
    new_game.addPlayer(dave)
    new_game.start(FRAME_RATE)

if __name__ == '__main__':
    main()
