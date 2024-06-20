import json
import os
import pygame

from modules.config import SCREEN_SIZE, STEP
from modules.mapmatrix import map
import sqlite3
import logging

logger = logging.getLogger("nameOfTheLogger")
logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

PATH = os.path.abspath(__file__ + '/../..')


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
        # del self


class Button:  # from yt @baraltech
    def __init__(self,
                 image,
                 pos,
                 text_input,
                 font: pygame.Font,
                 base_color: pygame.Color,
                 hovering_color: pygame.Color,
                 ):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font

        self.original_display = self.font.render(text_input, True, base_color)
        self.hover_display = self.font.render(text_input, True, hovering_color)
        self.hovering_color = hovering_color
        self.rect = self.original_display.get_rect(center=(self.x_pos, self.y_pos))
        self.image = pygame.transform.scale(image, self.rect.size)

        self.display = None

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        self.display = self.hover_display if is_hover else self.original_display

        screen.blit(self.display, self.rect)
        if is_hover and self.image:
            screen.blit(self.image, self.rect)

    def check_for_input(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
