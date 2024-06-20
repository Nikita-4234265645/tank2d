import pygame

from modules.classes import window
from modules.config import STEP


class Block(pygame.Rect):
    def __init__(self, x, y, type_block, image):
        super().__init__(x, y, STEP, STEP)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (STEP, STEP))
        self.type_block = type_block

    def blit(self):
        window.blit(self.image, (self.x, self.y))
