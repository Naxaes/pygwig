import typing
import pygame
import src.event

# Type hints
Vector = typing.Union[typing.Tuple[int, int], typing.List[int]]

presets = []


class WidgetManager(pygame.sprite.OrderedUpdates):

    def __init__(self, *widgets):
        super(WidgetManager, self).__init__(widgets)

        self.previous_keys = None
        self.focused = type('', (), {'update': lambda: None, 'unfocus': lambda: None})  # Temporary dummy object.
        self._focused_index = 0

    def _check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[9] and not self.previous_keys[9]:  # 9 is tab
            self.focused.unfocus()
            self._focused_index = (self._focused_index + 1) % len(self)
            self.focused = self.sprites()[self._focused_index]

        self.previous_keys = keys

    def _check_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            for i, widget in enumerate(self):
                if widget.rect.collidepoint(*pygame.mouse.get_pos()) and i != self._focused_index:
                    self.focused.unfocus()
                    self._focused_index = i
                    self.focused = self.sprites()[self._focused_index]

    def update(self):
        self._check_keys()
        self._check_mouse()
        self.focused.update()
        for widget in self:
            if widget.should_update:
                widget.update()


class BaseWidget(pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0), size=(0, 0)):
        super(BaseWidget, self).__init__()
        self._rect = pygame.Rect(pos, size)
        self._image = pygame.Surface(self._rect.size)
        self.should_update = True

        all_widgets.add(self)

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
    

class Slider(BaseWidget):

    def __init__(self, point_list, **kwargs):
        super(Slider, self).__init__(**kwargs)

        # Background
        self.background = self._image.copy()
        self.background.fill((100, 100, 100))

        # Other
        self.point_list = point_list
        self.segment_length = self._rect.size[0] / len(point_list)
        self.segments = len(point_list) - 1  # Reversed for easier check in 'self.move_slider()'.
        self.pressed = False
        self.current_value = self.point_list[0]

        # Slider
        self.slider_image = pygame.Surface((int(self.segment_length), self._rect.size[1]))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=self._rect.topleft)
        self.slider_rel_pos = (0, 0)

        # Make ready
        self.update_image()

    def move_slider(self):
        rect = self._rect
        mouse_segment_pos = int(min(max(0, (pygame.mouse.get_pos()[0] - rect.x) / self.segment_length), self.segments))
        self.slider.x = rect.x + mouse_segment_pos * self.segment_length
        self.current_value = self.point_list[mouse_segment_pos]

    def update_image(self):
        self._image.blit(self.background, (0, 0))
        self._image.blit(self.slider_image, (self.slider.x - self._rect.x, 0))  # Relative position.

    def update(self):
        if self.pressed:
            self.move_slider()
            self.update_image()

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.slider.collidepoint(*mouse_pos):
                self.pressed = True
            elif self._rect.collidepoint(*mouse_pos):
                self.move_slider()
                self.update_image()
        else:
            self.pressed = False


class ContinuousSlider(BaseWidget):

    def __init__(self, start, end, **kwargs):
        super(ContinuousSlider, self).__init__(**kwargs)

        # Background
        self.background = self._image.copy()
        self.background.fill((0, 0, 0))

        # Other
        self.start = start
        self.end = end
        self.pressed = False
        self.current_value = start

        # Slider
        self.slider_image = pygame.Surface((self._rect.size[0] // 12, self._rect.size[1]))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=self._rect.topleft)
        self.slider_rel_pos = (0, 0)

        # Make ready
        self.update_image()

    def move_slider(self):
        rect = self._rect
        mouse_pos = min(max(0, (pygame.mouse.get_pos()[0] - rect.x)), self._rect.width - self.slider.width)
        self.slider.x = rect.x + mouse_pos - self.slider.width // 2
        try:
            self.current_value = self.start + (mouse_pos / (self._rect.width - self.slider.width)) * (self.end - self.start)
        except ZeroDivisionError:
            self.current_value = self.start

    def update_image(self):
        self._image.blit(self.background, (0, 0))
        self._image.blit(self.slider_image, (self.slider.x - self._rect.x, 0))  # Relative position.

    def update(self):
        if self.pressed:
            self.move_slider()
            self.update_image()

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.slider.collidepoint(*mouse_pos):
                self.pressed = True
            elif self._rect.collidepoint(*mouse_pos):
                self.move_slider()
                self.update_image()
        else:
            self.pressed = False


class VerticalSlider(BaseWidget):

    def __init__(self, start, end, **kwargs):
        super(VerticalSlider, self).__init__(**kwargs)

        # Background
        self.background = self._image.copy()
        self.background.fill((100, 100, 100))

        # Other
        self.start = start
        self.end = end
        self.pressed = False
        self.current_value = start

        # Slider
        self.slider_image = pygame.Surface((self._rect.size[0], self._rect.size[1] // 12))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=self._rect.topleft)

        # Make ready
        self.update_image()

    def move_slider(self):
        rect = self._rect
        mouse_pos = min(max(0, (pygame.mouse.get_pos()[1] - rect.y)), self._rect.height - self.slider.height)
        self.slider.y = rect.y + mouse_pos
        try:
            self.current_value = self.start + (mouse_pos / (self._rect.height - self.slider.height)) * (self.end - self.start)
        except ZeroDivisionError:
            self.current_value = self.start

    def update_image(self):
        self._image.blit(self.background, (0, 0))
        self._image.blit(self.slider_image, (0, self.slider.y - self._rect.y))  # Relative position.

    def update(self):
        if self.pressed:
            self.move_slider()
            self.update_image()

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.slider.collidepoint(*mouse_pos):
                self.pressed = True
            elif self._rect.collidepoint(*mouse_pos):
                self.move_slider()
                self.update_image()
        else:
            self.pressed = False


class Button(BaseWidget):

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)

        self.color = pygame.Color(100, 0, 100)
        self.highlight_color = pygame.Color(50, 50, 50)

        self.hovered = False
        self.is_pressed = False

        self.update_image()

    def update_image(self):
        if self.is_pressed:
            self._image.fill(self.color + self.highlight_color)
        elif self.hovered:
            self._image.fill(self.color)
        else:
            self._image.fill(self.color - self.highlight_color)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        previous_hovered = self.hovered
        if self._rect.collidepoint(*mouse_pos):
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


class TextInput(BaseWidget):

    VALID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.+-,'

    def __init__(self, **kwargs):
        """
        Limitations: only 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.+-' and shift, tab,
                     return are supported.
        :param size:
        :param pos:
        """
        super(TextInput, self).__init__(**kwargs)
        self.size = self._rect.size

        self.color = {
            "text": pygame.Color("black"),
            "border": pygame.Color("dark grey"),
            "border_focused": pygame.Color("light grey"),
            "background": pygame.Color("white")
        }

        self._image.fill(self.color["background"])
        self.previous_keys = pygame.key.get_pressed()
        self.font = pygame.font.SysFont("Arial", 4 * self.size[1] // 5)
        self.text = []
        self.text_image = pygame.Surface(self.size)

        self.command_chars = {"backspace": self.backspace}

        self.caret = pygame.Rect((4, 2), (1, self.size[1] - 5))
        self.caret_time = pygame.time.get_ticks()
        self.caret_shown = True

    def backspace(self):
        try:
            self.text.pop(-1)
            self._image.fill(self.color["background"])
        except IndexError:
            pass

    def update_image(self):
        self.text_image = self.font.render("".join(self.text), 1, self.color["text"], self.color["background"])
        self._image.blit(self.text_image, (4, (self.size[1] - self.text_image.get_height()) // 2))
        pygame.draw.rect(self._image, self.color['border'], self._image.get_rect(topleft=(-1, -1)), 4)
        if self.caret_shown:
            self.caret.left = self.text_image.get_rect().right + 4
            pygame.draw.rect(self._image, (0, 0, 0), self.caret)
        else:
            pygame.draw.rect(self._image, self.color["background"], self.caret)

    def update(self):
        update_image = False
        keys = pygame.key.get_pressed()
        shift_pressed = keys[303] or keys[304] or keys[301]  # 303 is right shift. 304 is left shift. 301 is caps lock.
        for key, is_pressed in enumerate(keys):
            if is_pressed:
                print(key, pygame.key.name(key), self.previous_keys[key])
            if is_pressed and not self.previous_keys[key]:
                character = pygame.key.name(key)
                if shift_pressed:
                    try:
                        character = character.capitalize()
                        update_image = True
                    except ValueError:
                        pass
                if character in self.VALID_CHARS:
                    self.text.append(character)
                    update_image = True
                elif character in self.command_chars:
                    self.command_chars[character]()
                    update_image = True
                elif character == 'space':
                    self.text.append(' ')
                    update_image = True

        self.previous_keys = keys
        if update_image:
            self.update_image()

        if pygame.time.get_ticks() - self.caret_time >= 500:
            self.caret_shown = not self.caret_shown
            self.caret_time = pygame.time.get_ticks()
            self.update_image()

    def unfocus(self):
        self.caret_shown = False
        self.update_image()
        pygame.draw.rect(self._image, self.color['background'], self._image.get_rect(topleft=(-1, -1)), 4)


class TextInput2(TextBox):

    def __init__(self, **kwargs):
        """
        Limitations: only 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.+-' and shift, tab,
                     return are supported.
        :param size:
        :param pos:
        """
        super(TextInput2, self).__init__(**kwargs)

        self.command_chars = {"backspace": self.backspace}

        self.caret = pygame.Rect(self._text_area.topleft, (self._rect.width // 50, self._text_area.height - 4))
        self.caret_time = pygame.time.get_ticks()
        self.caret_shown = False

    def backspace(self):
        self._text = self.text[:-1]
        self.should_update = True

    def update(self):
        for event in src.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_BACKSPACE:
                self.backspace()
            else:
                self.text += event.unicode

        if pygame.time.get_ticks() - self.caret_time >= 500:
            self.caret_shown = not self.caret_shown
            self.caret_time = pygame.time.get_ticks()
            self.should_update = True

        if self.should_update:
            super(TextInput2, self).update()
            if self.caret_shown:
                if self._text:
                    rows = tuple(filter(None, self._text.split('\r')))
                    caret_height = self._font.size(rows[0])[1]
                    word_width = self._font.size(rows[-1])[0]
                    self.caret.left = self._text_area.left + word_width
                    self.caret.height = caret_height
                    self.caret.bottom = caret_height * len(rows) + self._border_size
                else:
                    self.caret.left = self._text_area.left
                pygame.draw.rect(self._image, (0, 0, 0), self.caret)
        self.should_update = False

    def unfocus(self):
        self.caret_shown = False
        super(TextInput2, self).unfocus()

all_widgets = WidgetManager()
