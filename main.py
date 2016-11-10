import pygame
import widgetmanager
pygame.init()

SIZE = WIDTH, HEIGHT = (720, 480)
FPS = 20
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

text_box1 = widgetmanager.TextInput2(pos=(20, 100), size=(256, 32))
text_box2 = widgetmanager.TextInput2(pos=(360, 240), size=(256, 32))
text_box3 = widgetmanager.TextInput2(pos=(20, 400), size=(256, 32))
widget_manager = widgetmanager.WidgetManager((text_box1, text_box2, text_box3))

while True:
    dt = clock.tick(FPS) / 1000
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    widget_manager.update()
    widget_manager.draw(screen)
    pygame.display.update()
