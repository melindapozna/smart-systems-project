from pygame import Vector2
from src.objects.bullet import Bullet
import time


class BasicNPC:
    def __init__(self, id, x, y, speed, player_sensor, border_sensor, character_collision_sensor):
        self.id = id
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.player_sensor = player_sensor
        self.border_sensor = border_sensor
        self.character_collision_sensor = character_collision_sensor
        self.hp = 50
        self.alive = True
        self.damage = 20
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        self.collided = False
        self.prev_collision_time = time.time()

    def move(self, dt):
        self.look_at(self.player_sensor.get_reading())
        self.pos += self.speed * dt * self.dir
        colliding_object = self.character_collision_sensor.get_reading(self.pos)

        # Shoot a bullet if a second has passed since the last one
        if self.collided and time.time() - self.prev_collision_time > 2:
            self.collided = False

        if not self.collided and not self.bullet_ready and time.time() - self.prev_shot_time > 1:
            self.bullet_ready = True

        # Kill the NPC if it reaches the border
        if self.border_sensor.get_reading(self.pos):
            self.alive = False

        if colliding_object and colliding_object.id != self.id:
            self.prev_collision_time = time.time()
            self.collide()


    # make the npc face a target position
    def look_at(self, position):
        dist = self.pos.distance_to(position)
        if self.collided:
            self.dir = -1 * (position - self.pos) / dist
            return
        if dist == 0:
            return
        self.dir = (position - self.pos) / dist

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def shoot_bullet(self, offset, collision_sensor):
        # offset: radius of the shooter to avoid bullet collision with the shooter itself
        self.bullet_ready = False
        self.prev_shot_time = time.time()

        return Bullet(self.pos + offset * self.dir, self.dir, self.damage, collision_sensor)

    def collide(self):
        self.collided = True
        self.look_at(self.player_sensor.get_reading().rotate(180))
        self.bullet_ready = False


    def accept(self, visitor):
        return visitor.visit_basic_npc(self)
