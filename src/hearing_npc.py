from pygame import Vector2
from src.bullet import Bullet
import time

class HearingNPC:
    def __init__(self, x, y, speed, sound_sensor, border_sensor):
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.sound_sensor = sound_sensor
        self.border_sensor = border_sensor
        self.hp = 50
        self.alive = True
        self.damage = 25
        self.bullet_ready = False
        self.prev_shot_time = time.time()

    def move(self, dt):
        self.look_at(self.player_sensor.get_reading())
        self.pos += self.speed * dt * self.dir

        # Shoot a bullet if a second has passed since the last one
        if not self.bullet_ready and time.time() - self.prev_shot_time > 1:
            self.bullet_ready = True

        # Kill the NPC if it reaches the border
        if self.border_sensor.get_reading(self.pos):
            self.alive = False

    def look_at(self, position):
        dist = self.pos.distance_to(position)
        if dist == 0:
            return
        self.dir = (position - self.pos) / dist

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def shoot_bullet(self, offset, collision_sensor):
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        return Bullet(self.pos + offset * self.dir, self.dir, self.damage, collision_sensor)

    def accept(self, visitor):
        visitor.visit_basic_npc(self)
