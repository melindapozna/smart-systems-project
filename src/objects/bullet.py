import time
from src.object_visitors.collisions.bullet_collision_visitor import BulletCollisionVisitor

class Bullet:
    def __init__(self, pos, direction, damage, radius, sensor, id):
        self.pos = pos
        self.dir = direction
        self.speed = 400
        self.radius = radius
        self.damage = damage
        self.sensor = sensor
        self.alive = True
        self.creation_time = time.time()
        self.id = id
        self.collision_visitor = BulletCollisionVisitor(self)

    def move(self, dt):
        self.pos += self.speed * dt * self.dir
        target_hit = self.sensor.get_reading(self)
        if target_hit:
            target_hit[0].accept(self.collision_visitor)
            #target_hit[0].take_damage(self.damage)
            #self.alive = False

        # self-destroy bullet after 10 seconds
        if time.time() - self.creation_time > 10:
            self.alive = False

    def accept(self, visitor):
        return visitor.visit_bullet(self)