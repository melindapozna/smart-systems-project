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
        self.prev_shot_time = time.time()
        self.type = "Basic"

    def move(self, dt):
        self.look_at(self.sensor.get_reading())
        self.pos += self.speed * dt * self.dir

        if not self.bullet_ready and time.time() - self.prev_shot_time > 1:
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
        self.prev_shot_time = time.time()
        return Bullet(self.pos.x, self.pos.y, self.dir, self.damage, DummySensor())

