import pygame


events = []


def update():
    global events
    events = []
    for event in pygame.event.get():
        events.append(event)


def get(event_type=None):
    if event_type:
        return (x for x in events if x.type == event_type)
    else:
        return tuple(events)