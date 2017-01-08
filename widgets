import pygame
import typing

# Type hints
Vector = typing.Union[typing.Tuple[int, int], typing.List[int]]

presets = []


class WidgetManager:

    def __init__(self, *widgets):
        self.shown_widgets = []
        self.hidden_widgets = []
        self.add(*widgets)

        self.previous_keys = [0] * 10
        self.is_focused = 0

    def _check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[9] and not self.previous_keys[9]:  # 9 is tab
            self.is_focused = (self.is_focused + 1) % len(self.shown_widgets)
        self.previous_keys = keys

    def _check_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            for i, widget in enumerate(self.shown_widgets):
                if widget.rect.collidepoint(*pygame.mouse.get_pos()):
                    self.is_focused = i

    def add(self, *widgets):
        for widget in widgets:
            self.shown_widgets.append(widget) if widget.show else self.hidden_widgets.append(widget)

    def remove(self, widget):
        pass

    def draw(self, surface):
        for widget in self.shown_widgets:
            surface.blit(widget.image, widget.rect)

    def update(self):
        self._check_keys()
        self._check_mouse()
        for widget in self.shown_widgets:
            widget.update()


class BaseWidget(pygame.sprite.Sprite):

    def __init__(self, **kwargs):
        super(BaseWidget, self).__init__()
        self.rect = pygame.Rect(kwargs.get('pos', (0, 0)), kwargs.get('size', (0, 0)))
        self.image = pygame.Surface(self.rect.size)
        self.show = kwargs.get('show', True)
        widgets.add(self)
    

class Slider(BaseWidget):

    def __init__(self, point_list, **kwargs):
        super(Slider, self).__init__(**kwargs)

        # Background
        self.background = self.image.copy()
        self.background.fill((100, 100, 100))

        # Other
        self.point_list = point_list
        self.segment_length = self.rect.size[0] / len(point_list)
        self.segments = len(point_list) - 1  # Reversed for easier check in 'self.move_slider()'.
        self.pressed = False
        self.current_value = self.point_list[0]

        # Slider
        self.slider_image = pygame.Surface((int(self.segment_length), self.rect.size[1]))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=self.rect.topleft)
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


class ContinuousSlider(BaseWidget):

    def __init__(self, start, end, **kwargs):
        super(ContinuousSlider, self).__init__(**kwargs)

        # Background
        self.background = self.image.copy()
        self.background.fill((0, 0, 0))

        # Other
        self.start = start
        self.end = end
        self.pressed = False
        self.current_value = start

        # Slider
        self.slider_image = pygame.Surface((self.rect.size[0] // 12, self.rect.size[1]))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=self.rect.topleft)
        self.slider_rel_pos = (0, 0)

        # Make ready
        self.update_image()

    def move_slider(self):
        rect = self.rect
        mouse_pos = min(max(0, (pygame.mouse.get_pos()[0] - rect.x)), self.rect.width - self.slider.width)
        self.slider.x = rect.x + mouse_pos - self.slider.width // 2
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


class VerticalSlider(BaseWidget):

    def __init__(self, start, end, **kwargs):
        super(VerticalSlider, self).__init__(**kwargs)

        # Background
        self.background = self.image.copy()
        self.background.fill((100, 100, 100))

        # Other
        self.start = start
        self.end = end
        self.pressed = False
        self.current_value = start

        # Slider
        self.slider_image = pygame.Surface((self.rect.size[0], self.rect.size[1] // 12))
        self.slider_image.fill((100, 255, 0))
        self.slider = self.slider_image.get_rect(topleft=self.rect.topleft)

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
            self.image.fill(self.color + self.highlight_color)
        elif self.hovered:
            self.image.fill(self.color)
        else:
            self.image.fill(self.color - self.highlight_color)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        previous_hovered = self.hovered
        if self.rect.collidepoint(*mouse_pos):
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

    def __init__(self, text='', font='', **kwargs) -> None:
        """
        A box to display text.

        Args:
            size: width and height.
            pos: x and y coordinates of the topleft corner.
            text: text to display.
            font: font of the text.
        """
        super(TextBox, self).__init__(**kwargs)
        self.image.fill((255, 255, 255))
        self._text = text
        if not font:
            self.font = 'Arial'
        else:
            self.font = font
        self.font_size = self.rect.height
        self.should_update = True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if text == self.text:
            return
        self._text = text
        self.should_update = True

    def _wrap_text(self):
        while True:
            font = pygame.font.SysFont(self.font, self.font_size)
            text_surface = font.render(self._text, 1, (0, 0, 0))
            if text_surface.get_height() > self.rect.height:
                self.font_size -= 1
                continue
            elif text_surface.get_width() > self.rect.width:
                if text_surface.get_height() * 2 > self.rect.height:
                    self.font_size -= 1
                    continue
                a = self.rect.width // text_surface.get_width()
                for i in range(a):
                    self.image.blit(
                        text_surface.subsurface(pygame.Rect((a*self.rect.width, 0), (self.rect.width, text_surface.get_height()))),
                        (2, text_surface.get_height() * a)
                    )
            else:
                self.image.blit(text_surface, (2, 0))
            break
        print('Height: ', text_surface.get_height(), self.rect.height)
        print('Width: ', text_surface.get_width(), self.rect.width)

    def update(self):
        if self.should_update:
            self.image.fill((255, 255, 255))
            self._wrap_text()
            self.should_update = False


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
        self.size = self.rect.size

        self.color = {
            "text": pygame.Color("black"),
            "border": pygame.Color("dark grey"),
            "border_focused": pygame.Color("light grey"),
            "background": pygame.Color("white")
        }

        self.image.fill(self.color["background"])
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
            self.image.fill(self.color["background"])
        except IndexError:
            pass

    def update_image(self):
        self.text_image = self.font.render("".join(self.text), 1, self.color["text"], self.color["background"])
        self.image.blit(self.text_image, (4, (self.size[1] - self.text_image.get_height()) // 2))
        pygame.draw.rect(self.image, self.color['border'], self.image.get_rect(topleft=(-1, -1)), 4)
        if self.caret_shown:
            self.caret.left = self.text_image.get_rect().right + 4
            pygame.draw.rect(self.image, (0, 0, 0), self.caret)
        else:
            pygame.draw.rect(self.image, self.color["background"], self.caret)

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


widgets = WidgetManager()
