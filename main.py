import os
import sys
from random import randint
import pygame
import pygame_gui

from modules.buttons import PLAY_BUTTON, QUIT_BUTTON
from modules.config import SCREEN_SIZE, STEP, TICK
from modules.classes import PATH, Movement
from modules.player import BasePlayer
from modules.block import Block
from modules.create_score_tabl import *
from modules.mapmatrix import LEVEL_MAP
from modules.utils import get_font


create_score_table()
background = pygame.image.load(os.path.join(PATH, 'images/background.webp'))
background = pygame.transform.scale(background, SCREEN_SIZE)

clock = pygame.time.Clock()
MANAGER = pygame_gui.UIManager(SCREEN_SIZE)
PLAYER1_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1200, 20), (300, 50)), manager=MANAGER,
                                                    object_id='#player1_entry')
PLAYER2_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1200, 480), (300, 50)), manager=MANAGER,
                                                    object_id='#player2_entry')

font = pygame.font.SysFont(None, 120)
winner_1_text = font.render('BLUE WINS', True, [0, 0, 255])
winner_2_text = font.render('RED WINS', True, [255, 0, 0])

wall_image1 = os.path.join(PATH, 'images/wall.png')
wall_image2 = os.path.join(PATH, 'images/wall_1.png')

window = pygame.display.set_mode(SCREEN_SIZE)


def generate_blocks(level_map, step, wall_1, wall_2):
    y_pos = 0
    for row in level_map:
        x_pos = 0
        for cell in row:
            if cell == 1:
                yield Block(x_pos, y_pos, 1, wall_1)
            elif cell == 2:
                yield Block(x_pos, y_pos, 2, wall_2)
            x_pos += step
        y_pos += step


blocks_list = list(generate_blocks(LEVEL_MAP, STEP, wall_image1, wall_image2))

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
                      sprite_path="images/tank1.png"
                      )

player_2 = BasePlayer(26, 14,
                      movement=Movement(
                          up=pygame.K_UP,
                          down=pygame.K_DOWN,
                          left=pygame.K_LEFT,
                          right=pygame.K_RIGHT,
                          shoot=pygame.K_l
                      ),
                      sprite_path="images/tank2.png"
                      )

is_game_running = True
winner = None


def play():
    global is_game_running
    global winner

    is_winner = False
    while is_game_running:
        window.blit(background, (0, 0))
        # ScoreManager.start_game()
        # ScoreManager.play()
        for block in blocks_list:
            block.blit()
            if block.colliderect(player_1.bullet):
                player_1.bullet.stop()
                if block.type_block == 1:
                    LEVEL_MAP[block.y // STEP][block.x // STEP] = 0
                    block.x = 500000
            if block.colliderect(player_2.bullet):
                player_2.bullet.stop()
                if block.type_block == 1:
                    LEVEL_MAP[block.y // STEP][block.x // STEP] = 0
                    # block.x = 500000
                    blocks_list.remove(block)
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
        clock.tick(TICK)
        # Game.end_game()
        pygame.display.flip()

    while is_winner:
        score = 0
        window.blit(background, (0, 0))
        cors = (list(SCREEN_SIZE)[0] // 2 - winner_1_text.get_width() // 2,
                list(SCREEN_SIZE)[1] // 2 - winner_1_text.get_width() // 2)
        if winner == 1:
            window.blit(winner_1_text, cors)
        elif winner == 2:
            window.blit(winner_2_text, cors)
        score = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_winner = False
        pygame.display.flip()


def main_menu():
    pygame.display.set_caption("Menu")

    MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))


    while True:
        window.blit(background, (0, 0))
        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input():
                    play()
                if QUIT_BUTTON.check_for_input():
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    get_user_name()


def get_user_name():
    while True:
        UI_REFRESH_RATE = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#player1_entry':
                BasePlayer.update_score_table(id=randint, nickname=event.text, score=0)
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == '#player2_entry':
                BasePlayer.update_score_table(id=randint, nickname=event.text, score=0)

            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)
        MANAGER.draw_ui(background)

if __name__ == "__main__":
    pygame.init()
    main_menu()
