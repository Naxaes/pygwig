import pygame

widget = pygame.sprite.Group()


class Button(pygame.sprite.Sprite):

    def __init__(self, size, pos):
        super(Button, self).__init__(widget)

        self.color = pygame.Color(100, 0, 100)
        self.highlight_color = pygame.Color(50, 50, 50)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)

        self.hovered = False
        self.is_pressed = False

        self.update_image()

    def update_image(self):
        if self.is_pressed:
            self.image.fill(self.color + self.highlight_color)
        elif self.hovered:
            self.image.fill(self.color)
        else:
            self.image.fill(self.color - self.highlight_color)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        previous_hovered = self.hovered
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

        left_click = pygame.mouse.get_pressed()[0]
        previous_pressed = self.is_pressed
        if left_click and self.hovered:
            self.is_pressed = True
        elif not left_click:
            self.is_pressed = False

        if previous_hovered != self.hovered or previous_pressed != self.is_pressed:
            self.update_image()
