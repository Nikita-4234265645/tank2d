import pygame
import os
import random
from modules.mapmatrix import *
from modules.classes import *
import json



# def load_statistics('data.json'):
#     try:
#         with open('data.json', 'r') as file:
#             statistics = json.load(file)
#         return statistics
#     except FileNotFoundError:
#         return {"players": [])
#
# statistics = load_statistics('data.json')
#
# def save_statistics('data.json', statistics):
#     with open(file_path, 'w') as file:
#         json.dump(statistics, file, indent=4)
#
# def update_statistics(statistics, player_name, score, level, enemies_destroyed):
#     player_found = False
#     for player in statistics["players"]:
#         if player["name"] == player_name:
#             player["score"] = score
#             player["level"] = level
#             player["enemies_destroyed"] = enemies_destroyed
#             player_found = True
#             break
#     if not player_found:
#         statistics["players"].append({
#             "name": player_name,
#             "score": score,
#             "level": level,
#             "enemies_destroyed": enemies_destroyed
#         })





pygame.init()

background = pygame.image.load(os.path.join(PATH, 'images/background.webp'))
background = pygame.transform.scale(background, SCREEN_SIZE)

font = pygame.font.SysFont(None, 120)
winner_1_text = font.render('BLUE WINS', True, [0, 0, 255])
winner_2_text = font.render('RED WINS', True, [255, 0, 0])

x = 0
y = 0
blocks_list = []

wall_image1 = os.path.join(PATH, 'images/wall.png')
wall_image2 = os.path.join(PATH, 'images/wall_1.png')

#TODO remake to generator
def generate_blocks(map, STEP, wall_image1, wall_image2):
    y = 0
    for row in map:
        x = 0
        for cell in row:
            if cell == 1:
                yield Block(x, y, 1, wall_image1)
            elif cell == 2:
                yield Block(x, y, 2, wall_image2)
            x += STEP
        y += STEP

blocks_list = list(generate_blocks(map, STEP, wall_image1, wall_image2))

'''for row in map:
    for cell in row:
        if cell == 1:
            blocks_list.append(Block(x, y, 1, wall_image1))
        elif cell == 2:
            blocks_list.append(Block(x, y, 2, wall_image2))
        x += STEP
    y += STEP
    x = 0'''

player_1 = BasePlayer(1, 1,
                      movement=Movement(
                          up=pygame.K_w,
                          down=pygame.K_s,
                          left=pygame.K_a,
                          right=pygame.K_d,
                          shoot=pygame.K_SPACE
                      ),
                      sprite_path="images/tank1.PNG"
                      )

player_2 = BasePlayer(2, 1,
                      movement=Movement(
                          up=pygame.K_UP,
                          down=pygame.K_DOWN,
                          left=pygame.K_LEFT,
                          right=pygame.K_RIGHT,
                          shoot=pygame.K_l
                      ),
                      sprite_path="images/tank2.PNG"
                      )

clock = pygame.time.Clock()

is_game_running = True
winner = None
while is_game_running:
    window.blit(background, (0, 0))

    #window.fill((0, 0, 0))
    for block in blocks_list:
        block.blit()
        if block.colliderect(player_1.bullet):
            player_1.bullet.stop()
            if block.type_block == 1:
                map[block.y // STEP][block.x // STEP] = 0
                block.x = 500000
        if block.colliderect(player_2.bullet):
            player_2.bullet.stop()
            if block.type_block == 1:
                map[block.y // STEP][block.x // STEP] = 0
                block.x = 500000
        if player_1.colliderect(player_2.bullet):
            winner = 2
            is_game_running = False
            is_winner = True
        elif player_2.colliderect(player_1.bullet):
            winner = 1
            is_game_running = False
            is_winner = True
    player_1.blit()
    player_2.blit()
    player_1.bullet.move()
    player_2.bullet.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False
    clock.tick(15)
    pygame.display.flip()

while is_winner:
    window.blit(background, (0, 0))
    cors = (list(SCREEN_SIZE)[0] // 2 - winner_1_text.get_width() // 2, list(SCREEN_SIZE)[1] // 2 - winner_1_text.get_width() // 2)
    if winner == 1:
        window.blit(winner_1_text, cors)
    elif winner == 2:
        window.blit(winner_2_text, cors)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_winner = False
    pygame.display.flip()