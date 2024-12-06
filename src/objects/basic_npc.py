from pygame import Vector2
from src.objects.bullet import Bullet
import time


class BasicNPC:
    def __init__(self, id, x, y, speed, player_sensor, border_sensor, character_collision_sensor):
        self.id = "BNPC" + str(id)
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.player_sensor = player_sensor
        self.border_sensor = border_sensor
        self.character_collision_sensor = character_collision_sensor
        self.hp = 50
        self.alive = True
        self.damage = -1
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        self.collided = False
        self.prev_collision_time = time.time()
        self.turned_on_collision = False

    def move(self, dt):
        if not self.collided:
            self.look_at(self.player_sensor.get_reading())
        self.pos += self.speed * dt * self.dir
        colliding_object = self.character_collision_sensor.get_reading(self)

        # Shoot a bullet if the previous collision was at least 2 seconds ago
        # and if the previous shot was at least 1 second ago
        if self.collided and time.time() - self.prev_collision_time > 2:
            self.collided = False
            self.turned_on_collision = False
        elif not self.collided and not self.bullet_ready and time.time() - self.prev_shot_time > 1:
            self.bullet_ready = True

        # Kill the NPC if it reaches the border
        if self.border_sensor.get_reading(self.pos):
            self.alive = False

        if colliding_object:
            self.collide()

    # make the npc face a target position
    def look_at(self, position):
        dist = self.pos.distance_to(position)

        # face away from object collided with
        #if self.collided:
        #    self.dir = -1 * (position - self.pos) / dist
        #    return
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
        self.prev_collision_time = time.time()
        self.collided = True
        #self.look_at(self.player_sensor.get_reading())
        self.bullet_ready = False
        self.take_damage(1)
        player_position = self.player_sensor.get_reading()
        if not self.turned_on_collision:
            #print(self.pos - player_position)
            self.dir = -1 * self.dir
            self.turned_on_collision = True

    def accept(self, visitor):
        return visitor.visit_basic_npc(self)
