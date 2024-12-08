from pygame import Vector2
from src.objects.bullet import Bullet
from src.object_visitors.collisions.basic_npc_collision_visitor import BasicNPCCollisionVisitor
import time
import math
import random


class BasicNPC:
    def __init__(self, id, x, y, speed, player_sensor, border_sensor, character_collision_sensor, game_stats):
        self.id = id
        self.radius = 10
        self.pos = Vector2(x, y)
        self.speed = speed
        self.dir = Vector2(0, 1)
        self.player_sensor = player_sensor
        self.border_sensor = border_sensor
        self.character_collision_sensor = character_collision_sensor
        self.hp = 50
        self.alive = True
        self.damage = 10
        self.bullet_radius = 2
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        self.collided = False
        self.prev_collision_time = time.time()
        # Directions in which the NPC can't move
        self.constraints = []
        self.items = []
        self.collision_visitor = BasicNPCCollisionVisitor(self)
        self.fire_rate = 1
        self.game_stats = game_stats
        self.vision_radius = 400
        self.last_known_location = None
        self.last_check = time.time()

    def action(self, dt):
        b_Point = self.pos + self.vision_radius * self.dir.rotate(20)
        c_Point = self.pos + self.vision_radius * self.dir.rotate(-20)
        character_position = self.player_sensor.get_reading()
        side_1 = self.pos.distance_to(b_Point)
        side_2 = self.pos.distance_to(c_Point)
        side_3 = c_Point.distance_to(b_Point)
        side_4 = self.pos.distance_to(character_position)
        side_5 = b_Point.distance_to(character_position)
        side_6 = c_Point.distance_to(character_position)
        p1 = (side_1 + side_2 + side_3) / 2
        p2 = (side_1 + side_4 + side_5) / 2
        p3 = (side_3 + side_5 + side_6) / 2
        p4 = (side_2 + side_4 + side_6) / 2
        area1 = math.sqrt(p1 * (p1 - side_1) * (p1 - side_2) * (p1 - side_3))
        area2 = math.sqrt(p2 * (p2 - side_1) * (p2 - side_4) * (p2 - side_5))
        area3 = math.sqrt(p3 * (p3 - side_3) * (p3 - side_5) * (p3 - side_6))
        area4 = math.sqrt(p4 * (p4 - side_2) * (p4 - side_4) * (p4 - side_6))
        if area2 + area3 + area4 + 1 >= area1 >= area2 + area3 + area4 - 1:
            self.move(dt)
            self.last_known_location = character_position.copy()
        else:
            self.searching(dt)

    def searching(self, dt):
        if self.last_known_location is not None:
            self.look_at(self.last_known_location)
            self.pos += self.speed * dt * self.dir
            if self.last_known_location.distance_to(self.pos) < 2:
                self.last_known_location = None
        else:
            if time.time() - self.last_check > 3:
                self.dir = self.dir.rotate(random.randint(0, 180))
                self.last_check = time.time()

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def process_constraints(self, speed_vector):
        for constraint in self.constraints:
            normal_component = speed_vector.dot(constraint)
            if normal_component > 0:
                speed_vector -= normal_component * constraint
        self.constraints = []
        return speed_vector

    def move(self, dt):
        colliding_objects = self.character_collision_sensor.get_reading(self)
        if colliding_objects:
            for colliding_object in colliding_objects:
                colliding_object.accept(self.collision_visitor)

        self.look_at(self.player_sensor.get_reading())
        speed_vector = self.speed * self.dir
        speed_vector = self.process_constraints(speed_vector)
        self.pos += dt * speed_vector

        # Shoot a bullet if the previous shot was at least 1 second ago
        if time.time() - self.prev_shot_time > self.fire_rate:
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

    def shoot_bullet(self, collision_sensor, bullet_id):
        self.bullet_ready = False
        self.prev_shot_time = time.time()
        # offset: radius of the shooter to avoid bullet collision with the shooter itself
        offset = self.radius + self.bullet_radius
        bullet_pos = self.pos + offset * self.dir
        self.game_stats.track_bullet_fired()
        return Bullet(bullet_pos, self.dir, self.damage, self.bullet_radius, collision_sensor, bullet_id)

    def pick_up(self, item):
        self.items.append(item)

    def accept(self, visitor):
        return visitor.visit_basic_npc(self)
