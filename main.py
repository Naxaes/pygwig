from random import choice
import pygame
import src.event
import src.widgets as widgets
pygame.init()

SIZE = WIDTH, HEIGHT = (1024, 720)
FPS = 30
NUM_WIDGETS = 16

WIDGET_W = WIDTH // (NUM_WIDGETS + 1)
X_SPACE = WIDGET_W // (NUM_WIDGETS + 1)
WIDGET_H = HEIGHT // (NUM_WIDGETS + 1)
Y_SPACE = WIDGET_H // (NUM_WIDGETS + 1)

screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

anchors = ['topleft', 'topright', 'bottomright', 'bottomleft', 'center']
colors = tuple(pygame.color.THECOLORS.values())
words = [
    'Testing', 'Hello', 'Aloha', 'Programming', 'Pygame games', 'Creating widgets\nto test on',
    'A long sentence with many breaks.\nJust for testing how it handles it.\nWe have to do it sometimes.'
]
font_names = pygame.font.get_fonts()
paddings = [(x, y) for x in range(1) for y in range(1)]
border_sizes = list(range(1, 25))


def create_widgets(num):
    for row in range(num):
        for col in range(num):
            if col % 2 == 0:
                widgets.TextBox(
                    pos=(WIDGET_W*col + X_SPACE*(col+1), WIDGET_H*row + Y_SPACE*(row+1)), size=(WIDGET_W, WIDGET_H),
                    text=choice(words), font_name=choice(font_names), padding=choice(paddings), text_color=choice(colors),
                    background_color=choice(colors), border_color=choice(colors), border_size=choice(border_sizes),
                    anchor=choice(anchors)
                )
            else:
                widgets.TextInput2(
                    pos=(WIDGET_W*col + X_SPACE*(col+1), WIDGET_H*row + Y_SPACE*(row+1)), size=(WIDGET_W, WIDGET_H),
                    font_name=choice(font_names), padding=choice(paddings), text_color=choice(colors),
                    background_color=choice(colors), border_color=choice(colors), border_size=choice(border_sizes),
                    anchor=choice(anchors)
                )

create_widgets(NUM_WIDGETS)
pause = False
time = 0
pos = 0, 0
while True:
    dt = clock.tick(FPS) / 1000
    time += dt
    # if time >= 2:
    #     for widget in widgets.all_widgets:
    #         widget.text_color = choice(colors)
    #     time = 0

    src.event.update()
    for event in src.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                for widget in widgets.all_widgets:
                    if widget.rect.collidepoint(mouse_pos):
                        print(widget)
        elif event.type == pygame.VIDEORESIZE:
            SIZE = WIDTH, HEIGHT = event.size
            WIDGET_W = WIDTH // (NUM_WIDGETS + 1)
            X_SPACE = WIDGET_W // (NUM_WIDGETS + 1)
            WIDGET_H = HEIGHT // (NUM_WIDGETS + 1)
            Y_SPACE = WIDGET_H // (NUM_WIDGETS + 1)
            screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
            row = col = 0
            for widget in widgets.all_widgets:
                widget.move_to(WIDGET_W*col + X_SPACE*(col+1), WIDGET_H*row + Y_SPACE*(row+1))
                widget.resize_to(WIDGET_W, WIDGET_H)
                col += 1
                if col == NUM_WIDGETS:
                    col = 0
                    row += 1

    if pygame.mouse.get_pressed()[0]:
        for widget in widgets.all_widgets:
            if widget.rect.collidepoint(pygame.mouse.get_pos()) and type(widget) == type(widgets.TextBox):
                widget.text = choice(words)
                widget.font_name = choice(font_names)
                widget.text_color = choice(colors)
                widget.background_color = choice(colors)
                widget.border_color = choice(colors)
                widget.border_size = choice(border_sizes)
                widget.padding = choice(paddings)
                widget.anchor = choice(anchors)

    screen.fill((0, 0, 0))
    widgets.all_widgets.update()
    widgets.all_widgets.draw(screen)
    pygame.display.update()
