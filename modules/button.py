import pygame


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
