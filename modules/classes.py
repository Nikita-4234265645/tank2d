import json
import os
import pygame

from modules.config import SCREEN_SIZE
import logging

logger = logging.getLogger("nameOfTheLogger")
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

PATH = os.path.abspath(__file__ + '/../..')


window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Tanks')


class ScoreManager:
    def __init__(self):
        #############################################
        with open('data.json', 'r') as f:
            self.data = json.load(f)
        #############################################
        self.score = 0
        self.nickname = None

    def start_game(self):
        self.nickname = self.data['name']
        self.score = self.data.get(self.nickname, 0)

    def play(self):
        self.score = 50

    def end_game(self):
        if self.data.get(self.nickname, 0) < self.score:
            self.data[self.nickname] = self.score
        #############################################
        with open('data.json', 'w') as f:
            json.dump(self.data, f)


#############################################


class Movement:
    def __init__(self, up, down, left, right, shoot):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.shoot = shoot


