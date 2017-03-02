from timeit import timeit

setup1 = """
import pygame
pygame.init()
import src.widgets as widgets
surface = pygame.Surface((48, 48))
"""

statement1 = """
widgets.add(*(widgets.BaseWidget(pos=(5, 5), size=(32, 32), show=True) for _ in range(10)))
widgets.update()
widgets.draw(surface)
"""

setup2 = """
import pygame
pygame.init()
import src.widgets as widgets
surface = pygame.Surface((48, 48))
"""

statement2 = """
widgets.widgets.add(*(widgets.BaseWidget(pos=(5, 5), size=(32, 32), show=True) for _ in range(10)))
widgets.widgets.update()
widgets.widgets.draw(surface)
"""

a = timeit(stmt=statement1, setup=setup1, number=1000)
b = timeit(stmt=statement2, setup=setup2, number=1000)

print("Method 1: {} s \nMethod 2: {} s\nDifference: {}".format(a, b, a/b))
