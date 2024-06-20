import pygame

from modules.bullet import Bullet
from modules.classes import window
from modules.config import STEP


class Tank(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x * STEP, y * STEP, STEP, STEP)
        self.image = None
        self.position = [x, y]
        self.bullet = Bullet(x, y)
        self.angle = 0

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
