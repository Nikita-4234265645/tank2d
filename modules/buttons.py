import pygame

from modules.utils import get_font
from modules.button import Button

PLAY_BUTTON = Button(image=pygame.image.load("images/RECT.png"),
                     pos=(640, 250),
                     text_input="PLAY",
                     font=get_font(75),
                     base_color=pygame.Color("#d7fcd4"),
                     hovering_color=pygame.Color("White"),
                     )

QUIT_BUTTON = Button(image=pygame.image.load("images/tank1.png"),
                         pos=(640, 550),
                         text_input="QUIT",
                         font=get_font(75),
                         base_color=pygame.Color("#d7fcd4"),
                         hovering_color=pygame.Color("White"),

                         )