import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(x, y)
