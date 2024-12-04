from pygame import Vector2

class Bullet:
    def __init__(self, x, y, direction, damage, sensor):
        self.pos = Vector2(x, y)
        self.dir = direction
        self.speed = 900
        self.damage = damage
        self.sensor = sensor
        self.alive = True
        self.type = "Bullet"

    def move(self, dt):
        self.pos += self.speed * dt * self.dir
        target_hit = self.sensor.get_reading(self.pos)
        if target_hit:
            target_hit.take_damage(self.damage)
            self.alive = False



