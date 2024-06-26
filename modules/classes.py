import json
import os
import pygame
from tanks.modules.mapmatrix import map
import sqlite3
import logging

logger = logging.getLogger("nameOfTheLogger")
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

PATH = os.path.abspath(__file__ + '/../..')
SCREEN_SIZE = (1400, 800)
STEP = 50

window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Tanks')

class Game:
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
        self.table_name = 'players'
        self.db_name = 'db_players.sqlite'

    def create_score_table(self, id=int, nickname=str, score=int):
        conn = sqlite3.connect(self.db4.sqlite3)
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS "players" (
            VALUES (? ? ?)
             )
            """
            query_params = (id, nickname, score)
            conn.execute(create_table_query, query_params)
            conn.commit()
            conn.close()
        finally:
            conn.close()

    def update_score_table(self, id=int, nickname=str, score=int):
        conn = sqlite3.connect('db_players.sqlite')
        try:
            query = f'''
            UPDATE 'players' SET "nickname" = ? WHERE "score" = ?, "id" = ?'''
            conn.execute(query, (id, nickname, +score,))
            conn.commit()
        finally:
            conn.close()

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


class Button(): #from yt @baraltech
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos [0]
        self.y_pos = pos [1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self. text_input = text_input
        self. text = self. font.render (self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self. text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen. blit(self.image, self.rect)
        screen. blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self. rect.left, self.rect.right) and position[1] in range(self.rect. top, self.rect.bottom):
            self.text = self. font. render (self.text_input, True, self.hovering_color)
        else:
            self. text = self.font.render(self.text_input, True, self.base_color)