import os
import sqlite3

import pygame

from modules.classes import PATH
from modules.config import STEP
from modules.mapmatrix import LEVEL_MAP
from modules.tank import Tank


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
            if LEVEL_MAP[self.position[1] - 1][self.position[0]] == 0:
                self.y -= STEP
                self.position[1] -= 1
            self.rotate(0)
        elif keys[self.movement.down]:
            if LEVEL_MAP[self.position[1] + 1][self.position[0]] == 0:
                self.y += STEP
                self.position[1] += 1
            self.rotate(180)
        elif keys[self.movement.left]:
            if LEVEL_MAP[self.position[1]][self.position[0] - 1] == 0:
                self.x -= STEP
                self.position[0] -= 1
            self.rotate(90)
        elif keys[self.movement.right]:
            if LEVEL_MAP[self.position[1]][self.position[0] + 1] == 0:
                self.x += STEP
                self.position[0] += 1
            self.rotate(270)
        elif keys[self.movement.shoot]:
            self.shoot()
