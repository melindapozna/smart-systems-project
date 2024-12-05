import time


class Bullet:
    def __init__(self, pos, direction, damage, sensor):
        self.pos = pos
        self.dir = direction
        self.speed = 400
        self.damage = damage
        self.sensor = sensor
        self.alive = True
        self.creation_time = time.time()

    def move(self, dt):
        self.pos += self.speed * dt * self.dir
        target_hit = self.sensor.get_reading(self.pos)
        if target_hit:
            target_hit.take_damage(self.damage)
            self.alive = False

        # self-destroy bullet after 10 seconds
        if time.time() - self.creation_time > 10:
            self.alive = False

    def accept(self, visitor):
        return visitor.visit_bullet(self)
