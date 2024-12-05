import pygame


class Player:
    def __init__(self, x, y, border_sensor):
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(x, y)
        self.hp = 100
        self.alive = True
        self.speed = 150
        self.border_sensor = border_sensor

    def move(self, direction, dt):
        self.pos += self.speed * dt * direction
        if self.border_sensor.get_reading(self.pos):
            self.alive = False

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def accept(self, visitor):
        return visitor.visit_player(self)