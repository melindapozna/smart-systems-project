import pygame
from src.object_visitors.collisions.player_collision_visitor import PlayerCollisionVisitor


class Player:
    def __init__(self, id,  x, y, border_sensor):
        self.id = id
        self.x = x
        self.radius = 10
        self.y = y
        self.pos = pygame.Vector2(x, y)
        self.hp = 100
        self.alive = True
        self.speed = 150
        self.border_sensor = border_sensor
        self.collision_sensor = None
        self.constraints = []
        self.collision_visitor = PlayerCollisionVisitor(self)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def process_constraints(self, speed_vector):
        for constraint in self.constraints:
            normal_component = speed_vector.dot(constraint)
            if normal_component > 0:
                speed_vector -= normal_component * constraint
        self.constraints = []
        return speed_vector

    def move(self, direction, dt):
        if self.border_sensor.get_reading(self.pos):
            self.alive = False

        colliding_objects = self.collision_sensor.get_reading(self)
        if colliding_objects:
            for colliding_object in colliding_objects:
                colliding_object.accept(self.collision_visitor)

        speed_vector = self.speed * direction
        speed_vector = self.process_constraints(speed_vector)

        self.pos += dt * speed_vector

    def collide(self, obstacle_pos):
      pass

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def accept(self, visitor):
        return visitor.visit_player(self)