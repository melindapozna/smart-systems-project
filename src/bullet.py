from pygame import Vector2

class Bullet:
    def __init__(self, x, y, direction, damage, sensor):
        self.pos = Vector2(x, y)
        self.dir = direction
        self.speed = 600
        self.damage = damage
        self.sensor = sensor
        self.alive = True
        self.bullet_ready = False

    def move(self, dt):
        self.pos += self.speed * dt * self.dir
        target_hit = self.sensor.get_reading()
        if target_hit:
            target_hit.take_damage(self.damage)
            self.alive = False



