import pygame
pygame.init()


with open("information.txt") as f:
    with open("pygame_integers.txt", "w") as f2:
        for line in f.readlines():
            line = "pygame." + line.strip()
            integer = eval(line)
            name = eval("pygame.key.name({0})".format(line))
            output = "\"{2}\": {0},\n".format(integer, line, name)
            f2.write(output)