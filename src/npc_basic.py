from pygame import Vector2
from src.bullet import Bullet
import time

class BasicNPC:
    def __init__(self, x, y, speed, sensor):
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.sensor = sensor
        self.hp = 50
        self.alive = True
        self.damage = 20
        self.bullet_ready = False
        self.clock = time.clock()

    def move(self, dt):
        self.look_at(self.sensor.get_reading())
        self.pos += self.speed * dt * self.dir

        if self.pos.x % 10 == 0:
            self.bullet_ready = True

    def look_at(self, position):
        dist = self.pos.distance_to(position)
        if dist == 0:
            return
        self.dir = (position - self.pos) / dist

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def shoot_bullet(self):
        class DummySensor:
            def get_reading(self):
                return None

        self.bullet_ready = False
        return Bullet(self.pos.x, self.pos.y, self.dir, self.damage, DummySensor())

