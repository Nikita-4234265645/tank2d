import os
import pygame
from tanks.modules.mapmatrix import map

PATH = os.path.abspath(__file__ + '/../..')
SCREEN_SIZE = (1400, 800)
STEP = 50

window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Tanks')


class Block(pygame.Rect):
    def __init__(self, x, y, type_block, image):
        super().__init__(x, y, STEP, STEP)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (STEP, STEP))
        self.type_block = type_block

    def blit(self):
        window.blit(self.image, (self.x, self.y))


class Tank(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x * STEP, y * STEP, STEP, STEP)
        self.image = None
        self.position = [x, y]
        self.bullet = Bullet(x, y)
        self.angle = 0

    def move(self):
        pass

    def blit(self):
        window.blit(self.image, (self.x, self.y))
        self.move()

    def rotate(self, angle):
        rotate = (360 - self.angle + angle)
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, rotate)

    def shoot(self):
        if self.bullet.count == 0:
            self.bullet.x = self.x + STEP / 2 - 10
            self.bullet.y = self.y + STEP / 2 - 10
            self.bullet.count = 20
            self.bullet.direction = self.angle


class Movement:
    def __init__(self, up, down, left, right, shoot):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.shoot = shoot


class BasePlayer(Tank):
    def __init__(self, x, y, movement, sprite_path):
        super().__init__(x, y)
        self.image = pygame.image.load(os.path.join(PATH, sprite_path))
        self.image = pygame.transform.scale(self.image, (STEP, STEP))
        self.movement = movement

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.movement.up]:
            if map[self.position[1] - 1][self.position[0]] == 0:
                self.y -= STEP
                self.position[1] -= 1
            self.rotate(0)
        elif keys[self.movement.down]:
            if map[self.position[1] + 1][self.position[0]] == 0:
                self.y += STEP
                self.position[1] += 1
            self.rotate(180)
        elif keys[self.movement.left]:
            if map[self.position[1]][self.position[0] - 1] == 0:
                self.x -= STEP
                self.position[0] -= 1
            self.rotate(90)
        elif keys[self.movement.right]:
            if map[self.position[1]][self.position[0] + 1] == 0:
                self.x += STEP
                self.position[0] += 1
            self.rotate(270)
        elif keys[self.movement.shoot]:
            self.shoot()


class Bullet(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)
        self.image = pygame.image.load(os.path.join(PATH, 'images/bullet.webp'))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.direction = None
        self.speed = 50
        self.count = 0

    def move(self):
        if self.count != 0:
            window.blit(self.image, (self.x, self.y))
            if self.direction == 0:
                self.y -= self.speed
            elif self.direction == 90:
                self.x -= self.speed
            elif self.direction == 180:
                self.y += self.speed
            elif self.direction == 270:
                self.x += self.speed
            self.count -= 1
            if self.count == 0:
                self.stop()

    def stop(self):
        self.count = 0
        self.x = 5000
        #del self
