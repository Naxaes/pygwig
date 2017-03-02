import pygame

all_sprites = pygame.sprite.Group()


class BaseWidget(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), size=(0, 0)):
        super(BaseWidget, self).__init__()
        self._rect = pygame.Rect(pos, size)
        self._image = pygame.Surface(self._rect.size)
        self.should_update = True

        all_sprites.add(self)

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image

    def move_to(self, *pos):
        setattr(self._rect, 'topleft', pos)

    def move(self, *pos):
        self._rect.move_ip(*pos)

    def resize_to(self, *size):
        self._rect.size = size
        self._image = pygame.transform.scale(self._image, size)

    def resize(self, *size):
        self._rect.inflate(*size)
        self._image = pygame.transform.scale(self._image, self._rect.size)

    def unfocus(self):
        pass


class TextBox(BaseWidget):

    ATTRIBUTES = [
        'anchor', 'background_color', 'border_color', 'border_size', 'font_name', 'font_size', 'image', 'padding',
        'rect', 'text', 'text_color', 'wrap'
    ]

    def __init__(
            self, pos=(0, 0), size=(0, 0), text='', font_name='Arial', text_color=pygame.Color('black'),
            anchor='topleft', padding=(0, 0), background_color=pygame.Color('white'), border_color=pygame.Color('grey'),
            border_size=3, wrap=True
    ) -> None:

        super().__init__(pos=pos, size=size)
        # Colors.
        self._text_color = text_color
        self._background_color = background_color
        self._border_color = border_color

        # Text options.
        self._anchor = anchor
        self._padding = padding
        self._wrap = wrap

        # Pass.
        self._border_size = border_size  # In pixels.
        self._text = text
        self._font_name = font_name

        # Dependent data.
        self._text_area = self._image.get_rect(
            size=(size[0] - border_size - padding[0] * 2, size[1] - border_size - padding[1] * 2),
        )
        self._text_area.center = self._image.get_rect().center
        if text:
            self._font_size, self._text_surface = self.get_text_surface_and_font_size()
            self._font = pygame.font.SysFont(font_name, self._font_size)
        else:
            self._font_size = 256
            self._font = pygame.font.SysFont(font_name, self._font_size)
            self._text_surface = pygame.Surface((0, 0))

        self._image.fill(background_color)
        pygame.draw.rect(self._image, self._border_color, self._image.get_rect(), self._border_size)
        self._image.blit(self._text_surface, self._text_area)

    @property
    def border_size(self):
        return self._border_size

    @border_size.setter
    def border_size(self, value):
        self._border_size = value
        self.should_update = True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.should_update = True

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, value):
        self._font_name = value
        self.should_update = True

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self.should_update = True

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value
        self.should_update = True

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        self._background_color = background_color

        self._image.fill(background_color)
        pygame.draw.rect(self._image, self._border_color, self._image.get_rect(), self._border_size)
        self._image.blit(self._text_surface, self._text_area)

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        self._border_color = border_color

        self._image.fill(self._background_color)
        pygame.draw.rect(self._image, border_color, self._image.get_rect(), self._border_size)
        self._image.blit(self._text_surface, self._text_area)

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = value
        self.should_update = True

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value
        self.should_update = True

    def get_text_surface_and_font_size(self, font_size=256):
        size = self._text_area.size
        font_name = self._font_name
        font_color = self._text_color
        bg_color = self._background_color
        wrap = self._wrap
        text_array = [word.split() for word in self._text.splitlines()]
        SysFont = pygame.font.SysFont

        rows = len(text_array)
        appendable_rows = []
        width, height = size
        lower, upper = 0, font_size
        found = False
        while not found:
            font = SysFont(font_name, font_size)
            font_sizes = tuple(font.size(' '.join(row)) for row in text_array)  # Font size (width, height) of each row.
            text_width = max(size[0] for size in font_sizes)
            text_height = font_sizes[0][1] * rows

            if wrap:
                # The surface cannot fit an exact font size so we'll return the lower of the two.
                if upper - lower <= 1:
                    found = True
                # Width exceed but height will fit one extra row.
                elif text_width > width and text_height + text_height // rows <= height:
                    for row, x in enumerate(font_sizes):
                        if x[0] == text_width:
                            if len(text_array[row]) > 1:
                                if row + 1 in appendable_rows:
                                    word = text_array[row].pop()
                                    text_array[row + 1].insert(0, word)
                                else:
                                    word = text_array[row].pop()
                                    text_array.insert(row + 1, [word])
                                    appendable_rows.append(row + 1)
                                    rows += 1
                            else:
                                upper = font_size
                                font_size = (lower + upper) // 2
                            break
                elif text_width > width or text_height > height:
                    upper = font_size
                    font_size = (lower + upper) // 2
                elif text_width < width and text_height < height:
                    lower = font_size
                    font_size = (lower + upper) // 2
                else:
                    found = True
            else:
                # The surface cannot fit an exact font size so we'll return the lower of the two.
                if font_size == lower or font_size == upper:
                    found = True
                elif text_width < width and text_height < height:
                    lower = font_size
                    font_size = (lower + upper) // 2
                elif text_width > width or text_height > height:
                    upper = font_size
                    font_size = (lower + upper) // 2
                else:
                    found = True

        return_surface = pygame.Surface(size)
        return_surface.fill(bg_color)
        h = height // rows
        for row, text_row in enumerate(text_array):
            sub_surface = pygame.font.SysFont(font_name, lower).render(' '.join(text_row), 1, font_color)
            rect = self._text_area.copy()
            rect.height = h
            rect.topleft = (0, h * row)
            pos = sub_surface.get_rect()
            setattr(pos, self._anchor, getattr(rect, self._anchor))
            return_surface.blit(sub_surface, pos)

        return lower, return_surface

    # def _update_text_area(self):
    #     text_array = [word.split() for word in self._text.splitlines()]
    #     rows = len(text_array)
    #     height = self._text_area.height
    #
    #     h = height // rows
    #     for row, text_row in enumerate(text_array):
    #         sub_surface = self._font.render(' '.join(text_row), 1, self._text_color)
    #         rect = self._text_area.copy()
    #         rect.height = h
    #         rect.topleft = (0, h * row)
    #         pos = sub_surface.get_rect()
    #         setattr(pos, self._anchor, getattr(rect, self._anchor))
    #         self._text_surface.blit(sub_surface, pos)
    #     self._image.blit(self._text_surface, self._text_area)

    def update(self):
        if self.should_update:
            # update_whole_image
            self._text_area = self._image.get_rect(
                size=(self._rect.size[0] - self._border_size - self._padding[0] * 2,
                      self._rect.size[1] - self._border_size - self._padding[1] * 2)
            )
            self._text_area.center = self._image.get_rect().center
            if self._text:
                self._font_size, self._text_surface = self.get_text_surface_and_font_size()
                self._font = pygame.font.SysFont(self._font_name, self._font_size)
            else:
                self._font_size = 1
                self._font = pygame.font.SysFont(self._font_name, self._font_size)
                self._text_surface = pygame.Surface((0, 0))

            self._image.fill(self._background_color)
            pygame.draw.rect(self._image, self._border_color, self._image.get_rect(), self._border_size)
            self._image.blit(self._text_surface, self._text_area)

            self.should_update = False

    def __repr__(self):
        attributes = sorted(self.ATTRIBUTES)
        values = []
        for attribute in attributes:
            if attribute in self.__dict__:
                values.append(getattr(self, attribute))
            else:
                values.append(getattr(self, '_' + attribute))

        return '{}: \n{}\n'.format(
            self.__class__.__name__, '\n'.join('\t{} = {!r}'.format(name, value) for name, value in zip(attributes, values))
        )


def wrap_text(text, font):
    text_array = [word.split() for word in text.splitlines()]

    rows = len(text_array)
    appendable_rows = []
    width, height = size
    lower, upper = 0, font_size
    found = False
    while not found:
        font = pygame.font.SysFont(font_name, font_size)
        font_sizes = tuple(font.size(' '.join(row)) for row in text_array)  # Font size (width, height) of each row.
        text_width = max(size[0] for size in font_sizes)
        text_height = font_sizes[0][1] * rows

        # The surface cannot fit an exact font size so we'll return the lower of the two.
        if upper - lower <= 1:
            found = True
        # Width exceed but height will fit one extra row.
        elif text_width > width and text_height + text_height // rows <= height:
            for row, x in enumerate(font_sizes):
                if x[0] == text_width:
                    if len(text_array[row]) > 1:
                        if row + 1 in appendable_rows:
                            word = text_array[row].pop()
                            text_array[row + 1].insert(0, word)
                        else:
                            word = text_array[row].pop()
                            text_array.insert(row + 1, [word])
                            appendable_rows.append(row + 1)
                            rows += 1
                    else:
                        upper = font_size
                        font_size = (lower + upper) // 2
                    break
        elif text_width > width or text_height > height:
            upper = font_size
            font_size = (lower + upper) // 2
        elif text_width < width and text_height < height:
            lower = font_size
            font_size = (lower + upper) // 2
        else:
            found = True


    return_surface = pygame.Surface(size)
    return_surface.fill(bg_color)
    h = height // rows
    for row, text_row in enumerate(text_array):
        sub_surface = pygame.font.SysFont(font_name, lower).render(' '.join(text_row), 1, font_color)
        rect = self._text_area.copy()
        rect.height = h
        rect.topleft = (0, h * row)
        pos = sub_surface.get_rect()
        setattr(pos, self._anchor, getattr(rect, self._anchor))
        return_surface.blit(sub_surface, pos)

    return lower, return_surface




























