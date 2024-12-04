import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(x, y)
        self.hp = 100
        self.alive = True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False