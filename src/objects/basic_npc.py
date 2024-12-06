from pygame import Vector2
from src.objects.bullet import Bullet
import time


class BasicNPC:
    def __init__(self, id, x, y, speed, player_sensor, border_sensor, character_collision_sensor):
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
        self.turned_on_collision = False
        # Directions in which the NPC can't move
        self.constraints = []

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
                self.collide(colliding_object.pos)
        self.look_at(self.player_sensor.get_reading())
        speed_vector = self.speed * self.dir
        speed_vector = self.process_constraints(speed_vector)

        self.pos += dt * speed_vector

        # Shoot a bullet if the previous shot was at least 1 second ago
        if time.time() - self.prev_shot_time > 1:
            self.bullet_ready = True

        # Kill the NPC if it reaches the border
        if self.border_sensor.get_reading(self.pos):
            self.alive = False

    # make the npc face a target position
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
        return Bullet(bullet_pos, self.dir, self.damage, self.bullet_radius, collision_sensor, bullet_id)

    def collide(self, obstacle_pos):
        # Take damage on all collisons
        # TODO move into a visitor
        if time.time() - self.prev_collision_time > 0.5:
            self.prev_collision_time = time.time()
            self.take_damage(1)

        vector_to_obstacle = obstacle_pos - self.pos
        dist_to_obstacle = vector_to_obstacle.length()
        if dist_to_obstacle == 0:
            return # What even is this case
        self.add_constraint(1 / dist_to_obstacle * vector_to_obstacle)

    def accept(self, visitor):
        return visitor.visit_basic_npc(self)
