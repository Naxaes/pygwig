import pygame


class WidgetManager:

    def __init__(self, widgets):
        super(WidgetManager, self).__init__()
        self.widgets = widgets
        self.previous_keys = pygame.key.get_pressed()
        self.is_focused = 0
        self.widgets[0].is_focused = True

    def draw(self, surface):
        for widget in self.widgets:
            surface.blit(widget.image, widget.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[9] and not self.previous_keys[9]:  # 9 is tab
            self.widgets[self.is_focused].is_focused = False
            self.is_focused = (self.is_focused + 1) % len(self.widgets)
            self.widgets[self.is_focused].is_focused = True
        self.previous_keys = keys
        self.widgets[self.is_focused].update()


class TextInput(pygame.sprite.Sprite):

    def __init__(self):
        super(TextInput, self).__init__()
        self.text = []

    def update(self):
        events = []
        for event in pygame.event.get():
            events.append(event)
            if event.type == pygame.KEYDOWN:
                self.text.append(event.unicode)
        print("Text =", "".join(self.text))

        for event in events:
            pygame.event.post(event)


class TextInput2(pygame.sprite.Sprite):

    VALID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.+-,'

    def __init__(self, size, pos):
        """
        Limitations: only 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.+-' and shift, tab,
                     return are supported.
        :param size:
        :param pos:
        """
        super(TextInput2, self).__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)
        self.size = size

        self.is_focused = False
        self.previous_keys = pygame.key.get_pressed()
        self.font = pygame.font.SysFont("Arial", 4 * size[1] // 5)
        self.text = []
        self.text_image = pygame.Surface(size)

        self.command_chars = {"backspace": self.backspace}

    def backspace(self):
        try:
            self.text.pop(-1)
        except IndexError:
            pass

    def update(self):
        if not self.is_focused:
            return
        keys = pygame.key.get_pressed()
        shift_pressed = keys[303] or keys[304] or keys[301]  # 303 is right shift. 304 is left shift. 301 is caps lock.
        for key, is_pressed in enumerate(keys):
            if is_pressed and not self.previous_keys[key]:
                character = pygame.key.name(key)
                if shift_pressed:
                    try:
                        character = character.capitalize()
                    except ValueError:
                        pass
                if character in self.VALID_CHARS:
                    self.text.append(character)
                elif character in self.command_chars:
                    self.command_chars[character]()
                # else:
                #     print(key, character)
        self.previous_keys = keys

        self.image.fill(pygame.Color(0, 255, 255))
        self.text_image = self.font.render("".join(self.text), 1, pygame.Color(0, 0, 0))
        self.image.blit(self.text_image, (4, (self.size[1] - self.text_image.get_height()) // 2))
        pygame.draw.rect(self.image, (255, 0, 0), self.image.get_rect(topleft=(-1, -1)), 4)



