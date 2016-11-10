import pygame

widget = pygame.sprite.Group()
presets = []


class Slider(pygame.sprite.Sprite):

    def __init__(self, pos, size, point_list):
        super(Slider, self).__init__(widget)

        # Main widget
        self.rect = pygame.Rect(pos, size)
        self.image = pygame.Surface(size)

        # Background
        self.background = pygame.Surface(size)
        self.background.fill((100, 100, 100))

        # Other
        self.point_list = point_list
        self.segment_length = size[0] / len(point_list)
        self.segments = len(point_list) - 1  # Reversed for easier check in 'self.move_slider()'.
        self.pressed = False
        self.current_value = self.point_list[0]

        # Slider
        self.slider_image = pygame.Surface((int(self.segment_length), size[1]))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=pos)
        self.slider_rel_pos = (0, 0)

        # Make ready
        self.update_image()

    def move_slider(self):
        rect = self.rect
        mouse_segment_pos = int(min(max(0, (pygame.mouse.get_pos()[0] - rect.x) / self.segment_length), self.segments))
        self.slider.x = rect.x + mouse_segment_pos * self.segment_length
        self.current_value = self.point_list[mouse_segment_pos]

    def update_image(self):
        self.image.blit(self.background, (0, 0))
        self.image.blit(self.slider_image, (self.slider.x - self.rect.x, 0))  # Relative position.

    def update(self):
        if self.pressed:
            self.move_slider()
            self.update_image()

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.slider.collidepoint(*mouse_pos):
                self.pressed = True
            elif self.rect.collidepoint(*mouse_pos):
                self.move_slider()
                self.update_image()
        else:
            self.pressed = False


class ContinuousSlider(pygame.sprite.Sprite):

    def __init__(self, pos, size, start, end):
        super(ContinuousSlider, self).__init__(widget)

        # Main widget
        self.rect = pygame.Rect(pos, size)
        self.image = pygame.Surface(size)

        # Background
        self.background = pygame.Surface(size)
        self.background.fill((100, 100, 100))

        # Other
        self.start = start
        self.end = end
        self.pressed = False
        self.current_value = start

        # Slider
        self.slider_image = pygame.Surface((size[0] // 12, size[1]))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=pos)
        self.slider_rel_pos = (0, 0)

        # Make ready
        self.update_image()

    def move_slider(self):
        rect = self.rect
        mouse_pos = min(max(0, (pygame.mouse.get_pos()[0] - rect.x)), self.rect.width - self.slider.width)
        self.slider.x = rect.x + mouse_pos
        try:
            self.current_value = self.start + (mouse_pos / (self.rect.width - self.slider.width)) * (self.end - self.start)
        except ZeroDivisionError:
            self.current_value = self.start

    def update_image(self):
        self.image.blit(self.background, (0, 0))
        self.image.blit(self.slider_image, (self.slider.x - self.rect.x, 0))  # Relative position.

    def update(self):
        if self.pressed:
            self.move_slider()
            self.update_image()

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.slider.collidepoint(*mouse_pos):
                self.pressed = True
            elif self.rect.collidepoint(*mouse_pos):
                self.move_slider()
                self.update_image()
        else:
            self.pressed = False


class VerticalSlider(pygame.sprite.Sprite):

    def __init__(self, pos, size, start, end):
        super(VerticalSlider, self).__init__(widget)

        # Main widget
        self.rect = pygame.Rect(pos, size)
        self.image = pygame.Surface(size)

        # Background
        self.background = pygame.Surface(size)
        self.background.fill((100, 100, 100))

        # Other
        self.start = start
        self.end = end
        self.pressed = False
        self.current_value = start

        # Slider
        self.slider_image = pygame.Surface((size[0], size[1] // 12))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=pos)

        # Make ready
        self.update_image()

    def move_slider(self):
        rect = self.rect
        mouse_pos = min(max(0, (pygame.mouse.get_pos()[1] - rect.y)), self.rect.height - self.slider.height)
        self.slider.y = rect.y + mouse_pos
        try:
            self.current_value = self.start + (mouse_pos / (self.rect.height - self.slider.height)) * (self.end - self.start)
        except ZeroDivisionError:
            self.current_value = self.start

    def update_image(self):
        self.image.blit(self.background, (0, 0))
        self.image.blit(self.slider_image, (0, self.slider.y - self.rect.y))  # Relative position.

    def update(self):
        if self.pressed:
            self.move_slider()
            self.update_image()

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.slider.collidepoint(*mouse_pos):
                self.pressed = True
            elif self.rect.collidepoint(*mouse_pos):
                self.move_slider()
                self.update_image()
        else:
            self.pressed = False
