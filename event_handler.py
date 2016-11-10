import pygame
from key_codes import codes
pygame.init()

event_list = {
    pygame.KEYDOWN: {},
    pygame.KEYUP: {},
    pygame.MOUSEBUTTONDOWN: {},
    pygame.MOUSEBUTTONUP: {},
    pygame.QUIT: {0: quit}
}

key_codes = codes


def convert_char_to_int(a):
    return key_codes[a]


def key_is_correct(key, check):
    if pygame.key.name(key) == check:
        return True
    else:
        pass


def add_key_event(key, function, modifier=None, key_up=False):
    key = key_codes[key]
    if not key_up:
        event_list[pygame.KEYDOWN][key] = function
    else:
        event_list[pygame.KEYUP][key] = function


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            function = event_list[pygame.KEYDOWN]
            if event.key in function:
                function[event.key]()
        elif event.type == pygame.KEYUP:
            function = event_list[pygame.KEYUP]
            if event.key in function:
                function[event.key]()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            function = event_list[pygame.MOUSEBUTTONDOWN]
            if event.button in function:
                function[event.button]()
        elif event.type == pygame.MOUSEBUTTONUP:
            function = event_list[pygame.MOUSEBUTTONUP]
            if event.button in function:
                function[event.button]()
        elif event.type == pygame.QUIT:
            function = event_list[pygame.QUIT]
            function[0]()
